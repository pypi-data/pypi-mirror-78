from django.contrib.contenttypes.models import ContentType
from jsonschema.validators import Draft7Validator

from huscy.attributes.models import AttributeSchema, AttributeSet
from huscy.pseudonyms.services import get_or_create_pseudonym


def get_or_create_attribute_set(subject):
    content_type = ContentType.objects.get_by_natural_key('attributes', 'attributeset')
    pseudonym = get_or_create_pseudonym(subject, content_type)

    attribute_set, created = AttributeSet.objects.get_or_create(pseudonym=pseudonym.code)
    return attribute_set


def update_attribute_set(attribute_set, attributes, attribute_schema_version=None):
    if attribute_schema_version is None:
        attribute_schema = attribute_set.attribute_schema
    else:
        if attribute_schema_version < attribute_set.attribute_schema.pk:
            raise Exception('New version for attribute schema must be greater than or equals with '
                            'current attribute schema version.')
        attribute_schema = AttributeSchema.objects.get(pk=attribute_schema_version)

    Draft7Validator(attribute_schema.schema).validate(attributes)

    attribute_set.attributes = attributes
    attribute_set.attribute_schema = attribute_schema
    attribute_set.save()

    return attribute_set


def add_choices_property_to_attribute_schema(name, choices, parent=None, required=None):
    return add_property_to_attribute_schema(name, 'string', parent, required, enum=choices)


def add_integer_property_to_attribute_schema(name, minimum=None, maximum=None, parent=None,
                                             required=False):
    kwargs = {}
    if minimum is not None:
        kwargs['minimum'] = minimum
    if maximum is not None:
        kwargs['maximum'] = maximum
    return add_property_to_attribute_schema(name, 'integer', parent, required, **kwargs)


def add_property_to_attribute_schema(property_name, property_type='object', parent=None,
                                     required=False, **kwargs):
    attribute_schema = get_attribute_schema().schema

    if parent is None:
        _add_to_properties(attribute_schema, property_name, property_type, required, **kwargs)
    else:
        _add_to_parent(attribute_schema, property_name, property_type, parent, required, **kwargs)

    return AttributeSchema.objects.create(schema=attribute_schema)


def _add_to_properties(json_schema, property_name, property_type, required, **kwargs):
    json_schema['properties'][property_name] = {
        'type': property_type,
    }

    for key, value in kwargs.items():
        json_schema['properties'][property_name][key] = value

    if required:
        json_schema.setdefault('required', [])
        json_schema['required'].append(property_name)


def _add_to_parent(json_schema, property_name, property_type, parent, required, **kwargs):
    if parent not in json_schema['properties']:
        raise Exception(f'This parent property does not exist: ({parent}).')

    json_schema_parent = json_schema['properties'][parent]

    if not 'object' == json_schema_parent['type']:
        raise Exception('Parent property must be of type "object". '
                        f'Current type is "{json_schema_parent["type"]}".')

    json_schema_parent.setdefault('properties', {})
    _add_to_properties(json_schema_parent, property_name, property_type, required, **kwargs)


def get_attribute_schema(version=None):
    queryset = AttributeSchema.objects

    try:
        if version is None:
            return queryset.latest('pk')
        else:
            return queryset.get(pk=version)
    except AttributeSchema.DoesNotExist:
        return _create_initial_attribute_schema()


def _create_initial_attribute_schema():
    if AttributeSchema.objects.exists():
        raise Exception('Initial attribute schema already exist!')

    return AttributeSchema.objects.create(schema={
        'type': 'object',
        'properties': {},
    })
