import pytest

from huscy.attributes.services import add_property_to_attribute_schema, get_attribute_schema

pytestmark = pytest.mark.django_db


def test_add_property_to_attribute_schema(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'object'},
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_property_with_type_string(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2', 'string')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'string'},
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_required_property(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2', 'string', required=True)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'string'},
        },
        'required': ['attribute2'],
    }

    assert expected == get_attribute_schema().schema


def test_add_property_to_parent(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2', 'string', parent='attribute1')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {
                'type': 'object',
                'properties': {
                    'attribute2': {'type': 'string'},
                },
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_required_property_to_parent(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2', 'string', parent='attribute1', required=True)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {
                'type': 'object',
                'properties': {
                    'attribute2': {'type': 'string'},
                },
                'required': ['attribute2'],
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_property_to_not_existing_parent(attribute_schema_v2):
    with pytest.raises(Exception) as e:
        add_property_to_attribute_schema('attribute2', 'string', parent='not_existing_property')

    assert 'This parent property does not exist: (not_existing_property).' == str(e.value)


def test_add_property_parent_that_is_not_type_object(attribute_schema_v3):
    with pytest.raises(Exception) as e:
        add_property_to_attribute_schema('attribute3', 'string', parent='attribute2')

    assert 'Parent property must be of type "object". Current type is "string".' == str(e.value)


def test_add_property_with_further_keyword_arguments(attribute_schema_v2):
    add_property_to_attribute_schema('attribute2', 'string', parent=None, required=False,
                                     extra1='extra1', extra2='extra2')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'string',
                'extra1': 'extra1',
                'extra2': 'extra2',
            },
        },
    }

    assert expected == get_attribute_schema().schema
