from __future__ import annotations

import textwrap
from collections import OrderedDict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping


class ConfigSchema:
    PATH = "schemas/config.schema.yaml"


# Populate a configuration option with standard jsonschema keys
# property, description, type, ...
@dataclass
class ConfigEntry:
    _fill_column = 70
    _comment_column = 40

    name: str = "main"
    level: int = 0
    description: str = None
    type: str | list | dict = None  # noqa: A003
    default: str | list = None
    properties: OrderedDict = field(default_factory=OrderedDict)

    def __post_init__(self):
        self.description = "".join(self.description.split("\n"))
        if self.default is None:
            self.default = "null"

    @property
    def indent(self):
        return "  "

    def commented_description(self, precomment=True):
        lines = textwrap.wrap(self.description, width=self._fill_column)
        if precomment:
            return "\n".join([f"# {line}" for line in lines])
        s = f"# {lines[0]}\n"
        if len(lines) > 0:
            s += "\n".join(
                [
                    "{0:>{fill}}{1}".format(" ", f"# {line}", fill=self._comment_column)
                    for line in lines[1:]
                ]
            )
        return s.strip()

    def __str__(self):
        if isinstance(self.default, dict):
            keyval = f"{self.indent * self.level}{self.name}:"
        else:
            keyval = f"{self.indent * self.level}{self.name}: {self.default}"
        if self.level == 0:
            s = f"{self.commented_description()}\n{keyval}"
        else:
            s = "{0:<{fill}}".format(keyval, fill=40)
            s += f"{self.commented_description(precomment=False)}"
        for prop in self.properties:
            s += f"\n{prop}"
        return s


class Config:
    """Class for storing configuration.

    NB: The parser cannot resolve references meaning only the
    properties sections will be populated.

    :param dict schema: A dict containing a JSONSchema object.

    """

    _fill_column = 70

    def __init__(self, schema: Mapping[str, Any] | None, name: str = "nbis") -> None:
        self._schema = schema
        self._description = "".join(self._schema.get("description").split("\n"))
        self._properties = self._parse_properties(
            schema.get("properties", OrderedDict())
        )
        self._name = name

    @property
    def description(self):
        return self._description

    @property
    def schema(self):
        return self._schema.get("$schema")

    @property
    def name(self):
        return self._name

    @property
    def properties(self):
        return self._properties

    def __str__(self):
        # FIXME: use project name from configuration file
        s = f"# {self.name} project admin configuration file\n\n"
        lines = textwrap.wrap(self.description, width=self._fill_column)
        s += "\n".join([f"# {line}" for line in lines]) + "\n"
        for prop in self.properties:
            s += f"\n{prop}\n"
        return s

    # Parse schema properties to config entries
    def _parse_properties(self, obj, level=-1):
        if isinstance(obj, str):
            return
        property_list = []
        level = level + 1
        for k, v in obj.items():
            if isinstance(v, dict):
                properties = v.pop("properties", None)
                entry = ConfigEntry(name=k, level=level, **v)
            else:
                properties = None
                entry = ConfigEntry(name=k, level=level, **v)
            if properties is not None:
                entry.properties = self._parse_properties(properties, level=level)
            property_list.append(entry)
        return property_list
