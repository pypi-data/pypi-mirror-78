import attr

from copy import deepcopy
from typing import Dict

from .attributes import CoreAttributes


@attr.s
class FlowFile(object):
    _attributes = attr.ib(factory=CoreAttributes.default_attributes)
    _content = attr.ib(default=b"")

    def __getitem__(self, item):
        return self.get_attribute(item)

    def get_attribute(self, item):
        return self._attributes.get(item)

    def get_attributes(self) -> Dict[str, str]:
        return self._attributes

    def put_attribute(self, key: str, value: str):
        return self.put_all_attributes(**{key: value})

    def put_all_attributes(self, **kwargs):
        new_attributes = deepcopy(self._attributes)
        new_attributes.update(kwargs)
        new_attributes.update(CoreAttributes.default_attributes())
        return FlowFile(new_attributes, self._content)

    def del_attribute(self, key):
        return self.del_all_attributes(keys={key})

    def del_all_attributes(self, keys: set):
        new_attributes: dict = deepcopy(self._attributes)
        for key in keys & new_attributes.keys():
            del new_attributes[key]
        new_attributes.update(CoreAttributes.default_attributes())
        return FlowFile(new_attributes, self._content)

    def get_content(self) -> bytes:
        return self._content
