import pytest

from huscy.attributes.services import get_or_create_attribute_set

pytestmark = pytest.mark.django_db


def test_return_existing_attribute_set(attribute_set, subject):
    result = get_or_create_attribute_set(subject)

    assert result == attribute_set


def test_return_new_created_attribute_set(django_db_reset_sequences, attribute_schema_v4,
                                          pseudonym):
    attribute_set = get_or_create_attribute_set(pseudonym.subject)

    assert attribute_set.pseudonym == '1234'
    assert attribute_set.attributes == {}
    assert attribute_set.attribute_schema == attribute_schema_v4
