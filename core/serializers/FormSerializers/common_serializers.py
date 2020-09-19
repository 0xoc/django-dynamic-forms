import json

from rest_framework import serializers

from core.models import Data, CharField, elements


class DataSerializer(serializers.ModelSerializer):
    """Element Extra data CRUD serializer"""

    class Meta:
        model = Data
        fields = ['pk', 'value', 'display']


class CharFieldSerializer(serializers.ModelSerializer):
    """Create Char field"""

    class Meta:
        model = CharField
        fields = ['pk', 'value', ]


class ElementsSetOrder(serializers.Serializer):
    """
    Receives a json array of elements and sets their orders

    structure of the elements_data

    elements_data = {
    "type":
    "pk":
    "order":
    }

    """
    elements_data = serializers.JSONField()

    @staticmethod
    def check_attr(json_data, attrs):
        syntax_errors = []

        for attr in attrs:
            if json_data.get(attr, None) == None:
                _error = "missing %s attr on \n %s" % (attr, json.dumps(json_data))
                syntax_errors.append(_error)
        return syntax_errors

    def validate_elements_data(self, elements_data):
        _elements = []
        # syntax check element data
        for element_data in elements_data:

            # syntax check the incoming element data
            _element_checks = self.check_attr(element_data, ["type", "pk", "order"])
            if _element_checks:
                raise serializers.ValidationError(_element_checks)

            # get the element model
            ElementModel = elements.get(element_data.get('type'))
            if not ElementModel:
                raise serializers.ValidationError("Element with type %s does not exist" % element_data.get('type'))

            # validate element pk
            try:
                el_pk = int(element_data.get('pk'))
            except (TypeError, ValueError):
                raise serializers.ValidationError("pk " + element_data.get('pk') + " is not a valid integer")

            # validate order
            try:
                el_order = int(element_data.get('order'))
            except (TypeError, ValueError):
                raise serializers.ValidationError("order " + element_data.get('order') + " is not a valid integer")

            try:
                _element_obj = ElementModel.objects.get(pk=el_pk)
                _elements.append({'element': _element_obj, 'order': el_order})

            except ElementModel.DoesNotExsit:
                raise serializers.ValidationError(
                    "Element with type %s and pk %d does not exist" % (element_data.get('type'),
                                                                       element_data.get('pk')))

        return _elements