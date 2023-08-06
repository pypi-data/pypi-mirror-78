import pytest
from model_bakery import baker

from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient

from huscy.attributes.models import AttributeSchema, AttributeSet


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Jim', last_name='Panse')


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def anonymous_client(user):
    return APIClient()


@pytest.fixture
def initial_json_schema():
    return {
        'type': 'object',
        'properties': {},
    }


@pytest.fixture
def json_schema_v2(initial_json_schema):
    json_schema = initial_json_schema.copy()
    json_schema['properties']['attribute1'] = {'type': 'object'}
    return json_schema


@pytest.fixture
def json_schema_v3(json_schema_v2):
    json_schema = json_schema_v2.copy()
    json_schema['properties']['attribute2'] = {'type': 'string'}
    return json_schema


@pytest.fixture
def json_schema_v4(json_schema_v3):
    json_schema = json_schema_v3.copy()
    json_schema['properties']['attribute3'] = {'type': 'number'}
    return json_schema


@pytest.fixture
def initial_attribute_schema(initial_json_schema):
    return AttributeSchema.objects.create(schema=initial_json_schema)


@pytest.fixture
def attribute_schema_v2(initial_attribute_schema, json_schema_v2):
    return AttributeSchema.objects.create(schema=json_schema_v2)


@pytest.fixture
def attribute_schema_v3(attribute_schema_v2, json_schema_v3):
    return AttributeSchema.objects.create(schema=json_schema_v3)


@pytest.fixture
def attribute_schema_v4(attribute_schema_v3, json_schema_v4):
    return AttributeSchema.objects.create(schema=json_schema_v4)


@pytest.fixture
def subject():
    return baker.make('subjects.Subject')


@pytest.fixture
def content_type():
    return ContentType.objects.get_by_natural_key('attributes', 'attributeset')


@pytest.fixture
def pseudonym(subject, content_type):
    return baker.make(
        'pseudonyms.Pseudonym',
        subject=subject,
        content_type=content_type,
        code='1234'
    )


@pytest.fixture
def attribute_set(attribute_schema_v4, pseudonym):
    return AttributeSet.objects.create(
        pseudonym=pseudonym.code,
        attributes={
            'attribute1': {},
            'attribute2': 'any string',
            'attribute3': 4.5,
        },
        attribute_schema=attribute_schema_v4,
    )
