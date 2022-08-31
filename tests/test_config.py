import pytest
from nbis.config import Config
from nbis.config import PropertyDict


@pytest.fixture
def data():
    d = dict(
        project_name='foo',
        docs=dict(src='docs')
    )
    return d


def test_config(data):
    conf = Config(data)
    assert isinstance(conf, PropertyDict)
    assert isinstance(conf.docs, PropertyDict)
