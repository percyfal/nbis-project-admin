import io

import jsonschema
import pkg_resources
import pytest
from nbis.config import Config
from nbis.config import Schema
from nbis.config import SchemaFiles
from ruamel.yaml import YAML


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
  url: null                             # webexport url
  port: 8080                            # HTTP port number
"""


@pytest.fixture(scope="session")
def pkg_schemafile():
    return pkg_resources.resource_filename("nbis", SchemaFiles.CONFIGURATION_SCHEMA)


@pytest.fixture(scope="session")
def pkg_schema(pkg_schemafile):
    with open(pkg_schemafile) as fh:
        schema = YAML().load(fh)
    return schema


@pytest.fixture(scope="session")
def schemaio():
    return io.StringIO(_SCHEMA)


@pytest.fixture(scope="session")
def schema(schemaio):
    return Schema(YAML().load(schemaio))


def test_empty_schema():
    schema = Schema(schema=None)
    assert schema is not None


def test_pkg_schema(tmp_path, pkg_schema):
    schema = Schema(pkg_schema)
    import sys

    cfg = Config.from_schema(schema, file=sys.stdout)
    assert cfg is not None


def test_schema(tmp_path, schema):
    p = tmp_path / "config.yaml"
    cfg = Config.from_schema(schema, project_name="foo", file=p)
    schema.validate(cfg)
    assert p.read_text() == _CONFIG.format(project_name="foo")
    cfg.save(p)
    cfg = Config(file=p)
    schema.validate(cfg)


def test_validation_error(schema):
    cfg = Config.from_schema(schema, project_name=123)
    with pytest.raises(jsonschema.exceptions.ValidationError):
        schema.validate(cfg)
