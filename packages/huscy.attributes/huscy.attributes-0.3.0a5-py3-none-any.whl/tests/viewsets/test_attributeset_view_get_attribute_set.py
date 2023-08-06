from model_bakery import baker

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.attributes.serializer import AttributeSchemaSerializer


def test_admin_user_can_retrieve_attribute_set(admin_client, attribute_set, subject):
    response = retrieve_attribute_set(admin_client, subject)

    assert HTTP_200_OK == response.status_code


def test_user_without_permission_can_retrieve_attribute_set(client, attribute_set, subject):
    response = retrieve_attribute_set(client, subject)

    assert HTTP_200_OK == response.status_code


def test_anonymous_user_cannot_retrieve_attribute_set(anonymous_client, attribute_set, subject):
    response = retrieve_attribute_set(anonymous_client, subject)

    assert HTTP_403_FORBIDDEN == response.status_code


def test_create_attribute_set_if_it_does_not_exist(django_db_reset_sequences, client,
                                                   attribute_schema_v2):
    subject = baker.make('subjects.Subject')

    response = retrieve_attribute_set(client, subject)

    expected = {
        'attributes': {},
        'attribute_schema': AttributeSchemaSerializer(attribute_schema_v2).data
    }

    assert HTTP_200_OK == response.status_code
    assert expected == response.json()


def retrieve_attribute_set(client, subject):
    return client.get(reverse('attributeset-detail', kwargs=dict(pk=subject.id)))
