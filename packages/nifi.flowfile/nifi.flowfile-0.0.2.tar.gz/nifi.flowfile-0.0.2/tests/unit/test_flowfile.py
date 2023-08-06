#!/usr/bin/env python

"""Tests for `nifi.flowfile` package."""
from io import BytesIO

import pytest
from click.testing import CliRunner
from nifi import flowfile
from nifi.flowfile import cli, FlowFile
from nifi.flowfile.stream import FlowFileStreamReader, FlowFileStreamWriter


@pytest.fixture
def flowfile_fragments():
    data = b"Hello World!"
    fragment_id = "abc"
    fragment_count = len(data)

    def attributes(index):
        return {
            "fragment.id": fragment_id,
            "fragment.count": f"{fragment_count}",
            "fragment.index": f"{index}",
        }

    return [
        (FlowFile(attributes(i), data[i].to_bytes(1, byteorder="big")))
        for i in range(fragment_count)
    ]


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.flowfile)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.flowfile, ["--help"])
    assert help_result.exit_code == 0


def test_pack_unpack_singleton():
    data = b"Hello World!"
    attributes = dict(abc="bca")
    ff = FlowFile(attributes=attributes, content=data)

    with BytesIO() as bytes_out:
        ff_writer = FlowFileStreamWriter(bytes_out)
        ff_writer.write(ff)
        encoded = bytes_out.getvalue()

    with BytesIO(encoded) as bytes_in:
        ff_reader = FlowFileStreamReader(bytes_in)
        ff_unpacked = ff_reader.read()
        bytes_in.close()

    assert ff_unpacked == ff


def test_pack_unpack_fragments(flowfile_fragments):
    with BytesIO() as bytes_out:
        ff_writer = FlowFileStreamWriter(bytes_out)
        ff_writer.write_all(flowfile_fragments)
        encoded = bytes_out.getvalue()

    with BytesIO(encoded) as bytes_in:
        ff_reader = FlowFileStreamReader(bytes_in)
        unpacked_flowfiles = list(ff_reader)

    assert flowfile_fragments == unpacked_flowfiles


def test_pack_unpack_file(flowfile_fragments, tmp_path):
    with flowfile.open(tmp_path / "test.pkg", mode="w") as f:
        f.write_all(flowfile_fragments)

    with flowfile.open(tmp_path / "test.pkg", mode="r") as f:
        unpacked_ff = list(f)

    assert flowfile_fragments == unpacked_ff
