import pytest

from huscy.attributes.services import add_integer_property_to_attribute_schema, get_attribute_schema

pytestmark = pytest.mark.django_db


def test_add_integer_property_to_attribute_schema(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'integer'},
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_integer_property_with_minimum_value(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2', minimum=15)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'integer',
                'minimum': 15,
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_integer_property_with_maximum_value(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2', maximum=15)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'integer',
                'maximum': 15,
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_integer_property_with_minimum_and_maximum_value(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2', minimum=5, maximum=15)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {
                'type': 'integer',
                'minimum': 5,
                'maximum': 15,
            },
        },
    }

    assert expected == get_attribute_schema().schema


def test_add_integer_property_as_required(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2', required=True)

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {'type': 'object'},
            'attribute2': {'type': 'integer'},
        },
        'required': ['attribute2'],
    }

    assert expected == get_attribute_schema().schema


def test_add_integer_property_to_parent(attribute_schema_v2):
    add_integer_property_to_attribute_schema('attribute2', parent='attribute1')

    expected = {
        'type': 'object',
        'properties': {
            'attribute1': {
                'type': 'object',
                'properties': {
                    'attribute2': {'type': 'integer'},
                },
            },
        },
    }

    assert expected == get_attribute_schema().schema
