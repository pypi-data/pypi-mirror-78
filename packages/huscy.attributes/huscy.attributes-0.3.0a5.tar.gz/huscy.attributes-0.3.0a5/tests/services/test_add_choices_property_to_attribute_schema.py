import pytest

from huscy.attributes.services import add_choices_property_to_attribute_schema, get_attribute_schema

pytestmark = pytest.mark.django_db


def test_add_choices_property_to_attribute_schema(attribute_schema_v2):
    add_choices_property_to_attribute_schema('attribute2', choices=['a', 'b', 'c'])

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'string',
                'enum': ['a', 'b', 'c'],
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_choices_property_as_required(attribute_schema_v2):
    add_choices_property_to_attribute_schema('attribute2', choices=['a', 'b', 'c'], required=True)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'string',
                'enum': ['a', 'b', 'c'],
            },
        },
        'required': ['attribute2'],
    }

    assert expected == get_attribute_schema().schema


def test_add_choices_property_to_parent(attribute_schema_v2):
    add_choices_property_to_attribute_schema('attribute2', choices=['a', 'b', 'c'],
                                             parent='attribute1')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {
                'type': 'object',
                'properties': {
                    'attribute2': {
                        'type': 'string',
                        'enum': ['a', 'b', 'c'],
                    },
                },
            },
        },
    }

    assert expected == get_attribute_schema().schema
