"""Module for handling configuration data."""

from __future__ import annotations

import copy
import csv
import json
import logging
import pprint
import types
from collections import OrderedDict
from typing import Any, Mapping

import jsonschema

try:
    import pkg_resources
except ImportError:
    from importlib import resources as pkg_resources
import ruamel.yaml
from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Base class for exceptions in this module."""


class SchemaFiles:  # pylint: disable=too-few-public-methods
    """Class for storing schema file names."""

    CONFIGURATION_SCHEMA = "schemas/config.schema.yaml"
    SNAKEMAKE_PROFILE_SCHEMA = "schemas/profile.schema.yaml"


# Need jsonschema>=4 for Draft202012Validator, but jupyter-book
# depends on jsonschema<4
DefaultSchemaValidator = jsonschema.validators.extend(
    jsonschema.validators.Draft7Validator
)


# Allow null schema; from tskit.metadata
def validate_bytes(data: bytes | None) -> None:
    """Validate that data is bytes."""
    if data is not None and not isinstance(data, bytes):
        raise TypeError(
            (f"If no encoding is set metadata should be bytes, found {type(data)}")
        )


class Schema:
    """Class for storing configuration schema.

    NB: The parser cannot resolve references meaning only the
    properties sections will be populated.

    :param dict schema: A dict containing a JSONSchema object.

    """

    def __init__(self, schema: Mapping[str, Any] | None) -> None:
        self._schema = schema
        if schema is None:
            self._string = ""
            self._validate_row = validate_bytes
        else:
            try:
                DefaultSchemaValidator(schema)
            except jsonschema.exceptions.SchemaError as ve:
                logger.error(ve)
                raise
            self._string = json.dumps(schema, sort_keys=True, separators=(",", ":"))
            self._validate_row = DefaultSchemaValidator(schema).validate
            if "type" in schema and "null" in schema["type"]:
                self.empty_value = None
            else:
                self.empty_value = {}

    def __repr__(self) -> str:
        return self._string

    def __str__(self) -> str:
        return pprint.pformat(self._schema)

    @property
    def schema(self):
        """Return a copy of the schema."""
        return copy.deepcopy(self._schema)

    def asdict(self) -> Mapping[str, Any] | None:
        """Return the schema as a dictionary."""
        return self.schema

    def validate(self, row: Any) -> dict:
        """Validate a configuration row (dict) against this schema."""
        try:
            self._validate_row(row)
        except jsonschema.exceptions.SchemaError as ve:
            logger.error(ve)
            raise
        return row

    def dump_properties(self, comments=True, example=False) -> dict:
        """Dump schema properties as dict.

        :param bool comments: include comments in output
        :param bool example: use property examples instead of defaults
        :return: A dictionary of properties and possibly  descriptions.

        :rtype: dict
        """
        if comments:
            properties = ruamel.yaml.comments.CommentedMap()
        else:
            raise NotImplementedError

        header = self.asdict().get("description", "")
        try:
            properties.yaml_set_start_comment(header)
        except IndexError:
            pass

        def update_properties(props, section, level):
            if isinstance(section, str):
                return None
            if not isinstance(section, dict):
                return None
            for k, v in section.items():
                if isinstance(v, dict):
                    desc = v.get("description", "")
                    if "properties" in v.keys():
                        props[k] = ruamel.yaml.comments.CommentedMap()
                        props[k] = update_properties(
                            props[k], v["properties"], level=level + 1
                        )
                        props.yaml_set_comment_before_after_key(before="\n", key=k)
                        props.yaml_set_comment_before_after_key(before=desc, key=k)
                    else:
                        if example:
                            props[k] = v.get("example", v.get("default", None))
                        else:
                            props[k] = v.get("default", None)

                        if level == 0:
                            props.yaml_set_comment_before_after_key(before="\n", key=k)
                            props.yaml_set_comment_before_after_key(before=desc, key=k)
                        else:
                            try:
                                props.yaml_set_comment_before_after_key(
                                    before=desc, key=k, indent=level * 2
                                )
                            except IndexError:
                                pass
            return props

        properties = update_properties(
            properties, self.asdict().get("properties", {}), level=0
        )
        return properties


def get_schema(schema="CONFIGURATION_SCHEMA"):
    """Get schema from file."""
    try:
        schemafile = pkg_resources.resource_filename(
            "nbis", str(getattr(SchemaFiles, schema))
        )
    except AttributeError:
        schemafile = pkg_resources.files("nbis") / str(getattr(SchemaFiles, schema))
    with open(schemafile, encoding="utf-8") as fh:
        schema = YAML().load(fh)
    return Schema(schema)


def load_config(file=None, data=None, schema="CONFIGURATION_SCHEMA", validate=True):
    """Load configuration from file or data."""
    schema = get_schema(schema)
    config = Config(file=file, data=data)
    if validate:
        schema.validate(config)
    return config


class PropertyDict(OrderedDict):
    """Simple class that allows for property access"""

    def __init__(self, data=None):
        if data is None:
            data = {}
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
        if key not in dir({}):
            try:
                setattr(self, key, value)
            except Exception as e:
                print(e)
                print(key, value)
                raise

    def asdict(self):
        """Return the PropertyDict as a dict."""
        return json.loads(json.dumps(self))


class Config(PropertyDict):
    """Class for storing configuration data."""

    def __init__(self, data=None, file=None):
        if data is None:
            data = {}
        if file is not None:
            fdata = self.read_from_file(file)
            data.update(**fdata)
        super().__init__(data)

    def read_from_file(self, file):
        """Read configuration from file."""
        yaml = YAML()
        try:
            if isinstance(file, str):
                with open(file, encoding="utf-8") as fh:
                    data = yaml.load(fh)
            else:
                data = yaml.load(file)
        except FileNotFoundError as e:
            logger.error(e)
            logger.info("setting data to empty dict")
            data = {}
        return data

    @classmethod
    def from_schema(cls, schema, file=None, tsv=False, example=False, **kwargs):
        """Create a configuration from a schema."""
        props = schema.dump_properties(example=example)
        props.update(**kwargs)
        if tsv:
            cls._dump_tsv(props, file)
        else:
            cls._dump_yaml(props, file)

        return Config(props)

    @classmethod
    def _dump_tsv(cls, d, file=None):
        if file is None:
            return
        writer = csv.DictWriter(file, fieldnames=d.keys(), delimiter="\t")
        writer.writeheader()
        allvals = []
        for _, v in d.items():
            allvals.append(v)
        rows = zip(*allvals)
        for r in rows:
            dd = dict(zip(d.keys(), r))
            writer.writerow(dd)

    @classmethod
    def _dump_yaml(cls, d, file=None):
        if file is None:
            return

        yaml = YAML()

        def represent_none(self, _):
            return self.represent_scalar("tag:yaml.org,2002:null", "null")

        yaml.representer.add_representer(type(None), represent_none)
        yaml.indent(sequence=0, offset=2)
        yaml.dump(d, file)

    def save(self, file):
        """Save configuration to file in YAML format."""
        self._dump_yaml(self.asdict(), file)

    @property
    def is_empty(self):
        """Return True if the configuration is empty."""
        return self.asdict() == {}
