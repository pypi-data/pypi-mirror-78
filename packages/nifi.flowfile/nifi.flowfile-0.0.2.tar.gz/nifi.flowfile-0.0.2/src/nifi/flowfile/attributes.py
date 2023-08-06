from uuid import uuid4
from enum import Enum


class CoreAttributes(Enum):
    """
    ref: https://github.com/apache/nifi/blob/main/nifi-commons/nifi-utils/src/main/java/org/apache/nifi/flowfile/attributes/CoreAttributes.java
    """  # noqa: E501

    PATH = "path"
    ABSOLUTE_PATH = "absolute.path"
    FILENAME = "filename"
    UUID = "uuid"
    PRIORITY = "priority"
    MIME_TYPE = "mime.type"
    DISCARD_REASON = "discard.reason"
    ALTERNATE_IDENTIFIER = "alternate.identifier"

    @staticmethod
    def default_attributes():
        uuid = str(uuid4())
        return {
            CoreAttributes.UUID: uuid,
            CoreAttributes.PATH: "./",
            CoreAttributes.FILENAME: uuid,
        }


class FragmentAttributes(Enum):
    """
    ref:
    """

    FRAGMENT_SIZE = "fragment.size"
    FRAGMENT_ID = "fragment.id"
    FRAGMENT_INDEX = "fragment.index"
    FRAGMENT_COUNT = "fragment.count"
    SEGMENT_ORIGINAL_FILENAME = "segment.original.filename"


class SiteToSiteAttributes(Enum):
    """
    ref:
    """

    S2S_HOST = "s2s.host"
    S2S_ADDRESS = "s2s.address"
    S2S_PORT_ID = "s2s.port.id"
