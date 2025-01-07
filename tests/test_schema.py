"""Test schema."""

import io
import sys

import jsonschema
try:
  import pkg_resources
except ImportError:
  from importlib import resources as pkg_resources
import pytest
from ruamel.yaml import YAML

from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles

_SCHEMA = """$schema: "http://json-schema.org/draft/2020-12/schema#"

description: |
  Schema short description.

  Schema multiline long description.

properties:
  project_name:
    description: Project name
    default: project_name
    type: string
  webexport:
    description: webexport configuration
    type: object
    default: {}
    properties:
      url:
        description: webexport url
        type: [string, 'null']
        default: null
      port:
        description: HTTP port number
        type: number
        default: 8080
"""

_CONFIG = """# Schema short description.

# Schema multiline long description.

# Project name
project_name: {project_name}

# webexport configuration
webexport:
  # webexport url
  url: null
  # HTTP port number
  port: 8080
"""


@pytest.fixture(scope="session", name="pkg_schemafile")
def fpkg_schemafile():
    """Pkg schemafile fixture"""
    try:
        return pkg_resources.resource_filename("nbis", SchemaFiles.CONFIGURATION_SCHEMA)
    except AttributeError:
        return pkg_resources.files("nbis") / SchemaFiles.CONFIGURATION_SCHEMA


@pytest.fixture(scope="session", name="pkg_schema")
def fpkg_schema(pkg_schemafile):
    """Pkg schema fixture"""
    with open(pkg_schemafile, encoding="utf-8") as fh:
        schema = YAML().load(fh)
    return schema


@pytest.fixture(scope="session", name="schemaio")
def fschemaio():
    """Schemaio fixture"""
    return io.StringIO(_SCHEMA)


@pytest.fixture(scope="session", name="schema")
def fschema(schemaio):
    """Schema fixture"""
    return Schema(YAML().load(schemaio))


def test_empty_schema():
    """Test empty schema."""
    schema = Schema(schema=None)
    assert schema is not None


def test_pkg_schema(pkg_schema):
    """Test pkg schema."""
    schema = Schema(pkg_schema)

    cfg = Config.from_schema(schema, file=sys.stdout)
    assert cfg is not None


def test_schema(tmp_path, schema):
    """Test schema."""
    p = tmp_path / "config.yaml"
    cfg = Config.from_schema(schema, project_name="foo", file=p)
    schema.validate(cfg)
    assert p.read_text() == _CONFIG.format(project_name="foo")
    cfg.save(p)
    cfg = Config(file=p)
    schema.validate(cfg)


def test_validation_error(schema):
    """Test validation error."""
    cfg = Config.from_schema(schema, project_name=123)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        schema.validate(cfg)
