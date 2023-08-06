from rest_framework import serializers


def validate_keys(serializer_instance):
    """
    Check that there are no additional keys included in the data
    """

    invalid_keys = {k for k in serializer_instance.initial_data.keys() if k not in serializer_instance.fields.keys()}

    if invalid_keys:
        raise serializers.ValidationError(f'Invalid keys {invalid_keys}')
