from __future__ import annotations

import logging
import os
import pathlib
import textwrap
import types
from collections import OrderedDict
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Mapping

import pkg_resources
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    pass


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
        self.description = " ".join(self.description.split("\n")).strip()
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


class ConfigSchema:
    """Class for storing configuration schema.

    NB: The parser cannot resolve references meaning only the
    properties sections will be populated.

    :param dict schema: A dict containing a JSONSchema object.

    """

    PATH = "schemas/config.schema.yaml"
    _fill_column = 70

    def __init__(self, schema: Mapping[str, Any] | None, name: str = "nbis") -> None:
        self._schema = schema
        self._description = " ".join(self._schema.get("description").split("\n"))
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


class PropertyDict(OrderedDict):
    """Simple class that allows for property access"""

    def __init__(self, data=None):
        if data is None:
            data = dict()
        super().__init__(data)
        if isinstance(data, types.GeneratorType):
            return
        for k, v in data.items():
            if isinstance(v, dict):
                v = PropertyDict(v)
            elif isinstance(v, list):
                val = []
                for x in v:
                    if isinstance(x, PropertyDict):
                        val.append(x)
                    elif isinstance(x, dict):
                        val.append(PropertyDict(x))
                    else:
                        val.append(x)
                v = val
            else:
                pass
            self[k] = v

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        if key not in dir(dict()):
            try:
                setattr(self, key, value)
            except Exception as e:
                print(e)
                print(key, value)
                raise


class Config(PropertyDict):
    DEFAULT_PATH = "nbis.yaml"

    def __init__(self, path=None):
        if path is None:
            path = self.DEFAULT_PATH
        else:
            if not os.path.exists(path):
                logger.warning(
                    f"'{path}' doesn't exist; trying default path '{self.DEFAULT_PATH}'"
                )
                path = self.DEFAULT_PATH
        with open(path) as fh:
            data = YAML().load(fh)
        super().__init__(data)
        self._project_root = pathlib.Path(path).parent

    @property
    def project_root(self):
        return self._project_root

    @classmethod
    def init(cls, dirname=None, **kw):
        """Save configuration representation of schema"""
        if kw.get("prog") is None:
            prog = "nbis"
            path = cls.DEFAULT_PATH
        else:
            prog = kw["prog"]
            path = f"{prog}.yaml"
        if dirname is not None:
            path = os.path.join(dirname, path)
        if os.path.exists(path):
            logger.warning(
                f"{pathlib.Path(path).absolute()} exists; please edit manually"
            )
            raise ConfigError
        schemafile = pkg_resources.resource_filename("nbis", ConfigSchema.PATH)
        with open(schemafile) as fh:
            schema = YAML().load(fh)
        config = ConfigSchema(schema, name=prog)
        # Use project command as default
        config.properties[0].default = prog
        with open(path, "w") as fh:
            fh.write(str(config))
