import pytest

from huscy.attributes import services
from huscy.attributes.models import AttributeSchema

pytestmark = pytest.mark.django_db


def test_create_new_schema_if_none_exists(mocker):
    spy = mocker.spy(services, '_create_initial_attribute_schema')

    assert not AttributeSchema.objects.exists()

    services.get_attribute_schema()

    assert 1 == len(AttributeSchema.objects.all())
    spy.assert_called_once()


def test_get_latest_schema(attribute_schema_v4):
    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'string'},
            'attribute3': {'type': 'number'},
        },
    }

    assert expected == services.get_attribute_schema().schema


def test_get_schema_by_version(django_db_reset_sequences, attribute_schema_v4):
    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
        },
    }

    assert expected == services.get_attribute_schema(version=2).schema
