"""Serialization code for NiFi's FlowFile Stream v3"""
import io
from io import RawIOBase

MAX_VALUE_2_BYTES = 65535
MAGIC_HEADER = b"NiFiFF3"


def write_field_length(writer, length: int):
    if length < MAX_VALUE_2_BYTES:
        writer.write(length.to_bytes(2, byteorder="big"))
    else:
        writer.write(MAX_VALUE_2_BYTES.to_bytes(2, byteorder="big"))
        if length.bit_length() > 32:
            raise ValueError("FlowFile-v3 only supports 32-bit field lengths")
        writer.write(length.to_bytes(4, byteorder="big"))


def read_field_length(reader: RawIOBase) -> int:
    rv = int.from_bytes(reader.read(2), byteorder="big")
    if rv == MAX_VALUE_2_BYTES:
        rv = int.from_bytes(reader.read(4), byteorder="big")
    return rv


def write_string(writer, value):
    value_bytes = value.encode("utf-8")
    write_field_length(writer, len(value_bytes))
    writer.write(value_bytes)


def read_string(reader):
    length = read_field_length(reader)
    rv = reader.read(length).decode("utf-8")
    return rv


def write_long(writer, value):
    if value.bit_length() > 64:
        raise ValueError("FlowFile-v3 format only supports 64-bit content lengths")
    writer.write(value.to_bytes(8, byteorder="big"))


def read_long(reader):
    return int.from_bytes(reader.read(8), byteorder="big")


def write_attributes(writer, attributes):
    write_field_length(writer, len(attributes))
    for key, value in attributes.items():
        write_string(writer, key)
        write_string(writer, value)


def read_attributes(reader):
    num_attributes = read_field_length(reader)
    rv = {}
    for i in range(num_attributes):
        key = read_string(reader)
        value = read_string(reader)
        rv[key] = value
    return rv


def read_header(reader):
    header = b""
    for i in range(len(MAGIC_HEADER)):
        n = reader.read(1)
        if n == b"":
            if i == 0:
                return None
            raise IOError("Not in FlowFile-v3 format")
        header += n
    return header


class FlowFileStreamIOBase(object):
    """
    Base class with shared behavior for both the reader and writer.
    """

    _closed = False
    _should_close_fp = False
    _fp = None

    def close(self):
        if self._closed:
            return
        self._closed = True
        if self._should_close_fp:
            self._fp.close()

    def __repr__(self):
        name = getattr(self._fp, "name", None)
        if name:
            wrapping = repr(name)
        else:
            wrapping = "<{} at 0x{:x}>".format(type(self._fp).__name__, id(self._fp))
        return "<nifi.flowfile.stream.{} at 0x{:x} wrapping {}".format(
            type(self).__name__, id(self), wrapping
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


class FlowFileStreamReader(FlowFileStreamIOBase):
    """
    Reader for the NiFi FlowFiles Stream v3 format.
    """

    _next_header = None
    _have_read_something = False

    def __init__(self, reader, **kwargs):
        self._fp = reader

    def _has_more_data(self):
        return not (self._next_header is None and self._have_read_something)

    def read(self):
        header = (
            read_header(self._fp) if self._next_header is None else self._next_header
        )
        if header != MAGIC_HEADER:
            raise IOError("Not in FlowFile-v3 format")

        attributes = read_attributes(self._fp)

        content_length = read_long(self._fp)
        content = self._fp.read(content_length)

        self._next_header = read_header(self._fp)
        self._have_read_something = True

        return attributes, content

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_more_data():
            return self.read()
        else:
            raise StopIteration


class FlowFileStreamWriter(FlowFileStreamIOBase):
    """
   Writer for the FlowFile Stream v3 format.
   """

    def __init__(self, fp, **writer):
        self._fp = fp

    def write_all(self, iterable):
        for attributes, content in iterable:
            self.write(attributes, content)

    def write(self, attributes: dict, content: bytes):
        self._fp.write(MAGIC_HEADER)

        attributes = {} if attributes is None else attributes
        write_attributes(self._fp, attributes)

        write_long(self._fp, len(content))
        self._fp.write(content)


def open(name, mode="r", **kwargs):
    """
    Open a FlowFile Stream v3 file for reading or writing.
    """

    if mode not in {"r", "w", "a"}:
        raise ValueError("'mode' must be either 'r', 'w', or 'a'")
    fp = io.open(name, mode=mode + "b")
    if mode == "r":
        rv = FlowFileStreamReader(fp, **kwargs)
    else:
        rv = FlowFileStreamWriter(fp, **kwargs)
    rv._should_close_fp = True
    return rv
