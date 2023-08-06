from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_retrieve_attribute_schema(admin_client, attribute_schema_v4):
    response = retrieve_attribute_schema(admin_client)

    assert HTTP_200_OK == response.status_code


def test_user_without_permission_can_retrieve_attribute_schema(client, attribute_schema_v4):
    response = retrieve_attribute_schema(client)

    assert HTTP_200_OK == response.status_code


def test_anonymous_user_cannot_retrieve_attribute_schema(anonymous_client, attribute_schema_v4):
    response = retrieve_attribute_schema(anonymous_client)

    assert HTTP_403_FORBIDDEN == response.status_code


def retrieve_attribute_schema(client):
    return client.get(reverse('attributeschema-detail'))
