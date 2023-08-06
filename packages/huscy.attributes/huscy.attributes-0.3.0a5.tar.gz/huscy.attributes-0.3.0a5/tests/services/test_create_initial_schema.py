from datetime import datetime

import pytest

from huscy.attributes.models import AttributeSchema
from huscy.attributes.services import _create_initial_attribute_schema

pytestmark = pytest.mark.django_db


@pytest.mark.freeze_time('2000-01-01T10:00:00')
def test_create_initial_attribute_schema():
    assert not AttributeSchema.objects.exists()

    _create_initial_attribute_schema()

    attribute_schema = AttributeSchema.objects.get()
    assert attribute_schema.created_at == datetime(2000, 1, 1, 10)

    expected = {
        'type': 'object',
        'properties': {},
    }
    assert expected == attribute_schema.schema


def test_create_initial_attribute_schema_raises_error_if_one_exists():
    _create_initial_attribute_schema()

    with pytest.raises(Exception) as e:
        _create_initial_attribute_schema()

    assert 'Initial attribute schema already exist!' == str(e.value)
