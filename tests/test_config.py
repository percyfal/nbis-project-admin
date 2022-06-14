import io
import os

import pkg_resources
import pytest
from nbis.config import Config
from nbis.config import ConfigSchema
from ruamel.yaml import YAML


_SCHEMA = """$schema: "http://json-schema.org/draft/2020-12/schema#"

description: |
  Aliquam erat volutpat. Nunc eleifend leo vitae magna.
  In id erat non orci commodo lobortis. Proin neque massa, cursus ut,
  gravida ut, lobortis eget, lacus. Sed diam. Praesent fermentum
  tempor tellus. Nullam tempus. Mauris ac felis vel velit tristique
  imperdiet. Donec at pede. Etiam vel neque nec dui dignissim
  bibendum. Vivamus id enim. Phasellus neque orci, porta a, aliquet
  quis, semper a, massa. Phasellus purus. Pellentesque tristique
  imperdiet tortor. Nam euismod tellus id erat.

properties:
  project_name:
    description: |
      Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
      hendrerit tempor tellus. Donec pretium posuere tellus. Proin
      quam nisl, tincidunt et, mattis eget, convallis nec, purus. Cum
      sociis natoque penatibus et magnis dis parturient montes,
      nascetur ridiculus mus. Nulla posuere. Donec vitae dolor. Nullam
      tristique diam non turpis. Cras placerat accumsan nulla. Nullam
      rutrum. Nam vestibulum accumsan nisl.
    default: project_name
    type: str
  webexport:
    description: webexport configuration
    type: object
    default: {}
    properties:
      url:
        description: webexport url
        type: [str, 'null']
        default: null
      port:
        description: |
          Nullam eu ante vel est convallis dignissim. Fusce suscipit,
          wisi nec facilisis facilisis, est dui fermentum leo, quis
          tempor ligula erat quis odio. Nunc porta vulputate tellus.
          Nunc rutrum turpis sed pede. Sed bibendum. Aliquam posuere.
          Nunc aliquet, augue nec adipiscing interdum, lacus tellus
          malesuada massa, quis varius mi purus non odio. Pellentesque
          condimentum, magna ut suscipit hendrerit, ipsum augue ornare
          nulla, non luctus diam neque sit amet urna. Curabitur
          vulputate vestibulum lorem. Fusce sagittis, libero non
          molestie mollis, magna orci ultrices dolor, at vulputate
          neque nulla lacinia eros. Sed id ligula quis est convallis
          tempor. Curabitur lacinia pulvinar nibh. Nam a sapien.
        type: numeric
        default: 8080
      protocol:
        description: webexport protocol
        type: object
        default: {}
        properties:
          name:
            type: str
            description: Protocol name
            default: rsync
  confluence:
    description: confluence address
    default: null
    type: [str, 'null']
"""

_YAML = """# nbis project admin configuration file

# Aliquam erat volutpat. Nunc eleifend leo vitae magna. In id erat non
# orci commodo lobortis. Proin neque massa, cursus ut, gravida ut,
# lobortis eget, lacus. Sed diam. Praesent fermentum tempor tellus.
# Nullam tempus. Mauris ac felis vel velit tristique imperdiet. Donec at
# pede. Etiam vel neque nec dui dignissim bibendum. Vivamus id enim.
# Phasellus neque orci, porta a, aliquet quis, semper a, massa.
# Phasellus purus. Pellentesque tristique imperdiet tortor. Nam euismod
# tellus id erat.

# Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec
# hendrerit tempor tellus. Donec pretium posuere tellus. Proin quam
# nisl, tincidunt et, mattis eget, convallis nec, purus. Cum sociis
# natoque penatibus et magnis dis parturient montes, nascetur ridiculus
# mus. Nulla posuere. Donec vitae dolor. Nullam tristique diam non
# turpis. Cras placerat accumsan nulla. Nullam rutrum. Nam vestibulum
# accumsan nisl.
project_name: project_name

# webexport configuration
webexport:
  url: null                             # webexport url
  port: 8080                            # Nullam eu ante vel est convallis dignissim. Fusce suscipit, wisi nec
                                        # facilisis facilisis, est dui fermentum leo, quis tempor ligula erat
                                        # quis odio. Nunc porta vulputate tellus. Nunc rutrum turpis sed pede.
                                        # Sed bibendum. Aliquam posuere. Nunc aliquet, augue nec adipiscing
                                        # interdum, lacus tellus malesuada massa, quis varius mi purus non odio.
                                        # Pellentesque condimentum, magna ut suscipit hendrerit, ipsum augue
                                        # ornare nulla, non luctus diam neque sit amet urna. Curabitur vulputate
                                        # vestibulum lorem. Fusce sagittis, libero non molestie mollis, magna
                                        # orci ultrices dolor, at vulputate neque nulla lacinia eros. Sed id
                                        # ligula quis est convallis tempor. Curabitur lacinia pulvinar nibh. Nam
                                        # a sapien.
  protocol:                             # webexport protocol
    name: rsync                         # Protocol name

# confluence address
confluence: null
"""  # noqa: E501


@pytest.fixture(scope="session")
def schemaio():
    return io.StringIO(_SCHEMA)


@pytest.fixture(scope="session")
def schemafile():
    return pkg_resources.resource_filename("nbis", ConfigSchema.PATH)


@pytest.fixture
def config(schemafile):
    with open(schemafile) as fh:
        schema = YAML().load(fh)
    config = ConfigSchema(schema, name="nbis")
    config.properties[0].default = "nbis"
    return config


@pytest.fixture
def configfile(config, tmp_path):
    p = tmp_path / "nbis.yaml"
    p.write_text(str(config))
    return p


def test_parse_schema(schemaio):
    schema = YAML().load(schemaio)
    conf = ConfigSchema(schema)
    assert str(conf) == _YAML


def test_schema(schemafile):
    assert os.path.exists(schemafile)


def test_config(configfile):
    c = Config(configfile)
    assert c.project_root == configfile.parent
    assert c.bibliography == "references/bibliography.bib"
