import pytest

from huscy.attributes.models import AttributeSet

pytestmark = pytest.mark.django_db


def test_defaults_for_model_fields(attribute_schema_v3):
    attribute_set = AttributeSet.objects.create(pseudonym='123')

    assert attribute_set.attributes == {}
    assert attribute_set.attribute_schema == attribute_schema_v3
