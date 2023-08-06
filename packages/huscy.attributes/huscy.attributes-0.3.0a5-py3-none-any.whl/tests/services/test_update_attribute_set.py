import pytest

from jsonschema.exceptions import ValidationError

from huscy.attributes.services import add_choices_property_to_attribute_schema, update_attribute_set

pytestmark = pytest.mark.django_db


def test_update_attribute_set(attribute_set):
    attributes = attribute_set.attributes
    attributes['attribute3'] = 100.0

    update_attribute_set(attribute_set, attributes)

    expected = {
        'attribute1': {},
        'attribute2': 'any string',
        'attribute3': 100.0,
    }

    attribute_set.refresh_from_db()

    assert expected == attribute_set.attributes


def test_update_attribute_set_with_invalid_data(attribute_set):
    attributes = attribute_set.attributes
    attributes['attribute3'] = 'invalid'

    with pytest.raises(ValidationError):
        update_attribute_set(attribute_set, attributes)


def test_update_attribute_set_data_together_with_attribute_schema_version(attribute_set):
    latest_attribute_schema = add_choices_property_to_attribute_schema('attribute4', ['a', 'b'])

    attributes = attribute_set.attributes
    attributes['attribute4'] = 'a'

    update_attribute_set(attribute_set, attributes, latest_attribute_schema.pk)

    attribute_set.refresh_from_db()

    expected = {
        'attribute1': {},
        'attribute2': 'any string',
        'attribute3': 4.5,
        'attribute4': 'a',
    }

    assert attribute_set.attribute_schema == latest_attribute_schema
    assert expected == attribute_set.attributes


def test_update_attribute_schema_to_lower_version(attribute_set):
    with pytest.raises(Exception) as e:
        update_attribute_set(attribute_set, attribute_set.attributes,
                             attribute_set.attribute_schema.pk - 1)

    expected = ('New version for attribute schema must be greater than or equals with current '
                'attribute schema version.')

    assert expected == str(e.value)
