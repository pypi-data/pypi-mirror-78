from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_update_attribute_set(admin_client, attribute_set, subject):
    response = update_attribute_set(admin_client, attribute_set, subject)

    assert HTTP_200_OK == response.status_code


def test_user_without_permission_can_update_attribute_set(client, attribute_set, subject):
    response = update_attribute_set(client, attribute_set, subject)

    assert HTTP_200_OK == response.status_code


def test_anonymous_user_can_update_attribute_set(anonymous_client, attribute_set, subject):
    response = update_attribute_set(anonymous_client, attribute_set, subject)

    assert HTTP_403_FORBIDDEN == response.status_code


def update_attribute_set(client, attribute_set, subject):
    return client.put(
        reverse('attributeset-detail', kwargs=dict(pk=subject.id)),
        data={
            'attribute_schema_version': attribute_set.attribute_schema.pk,
            'attributes': {
                'attribute1': {},
                'attribute2': 'another string',
                'attribute3': 1.0
            },
        },
        format='json',
    )
