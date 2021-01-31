
from rest_framework import serializers
from .models import Manufacturer, EqMark, EqModel, EqType


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['name', 'id']


class EqModelSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()

    class Meta:
        model = EqModel
        fields = ['id', 'eqmodel', 'manufacturer']


class TypeSerializer(serializers.ModelSerializer):

    eqmodel = EqModelSerializer()

    class Meta:
        model = EqType
        fields = ['id', 'eqtype', 'eqmodel', 'manufacturer']


class MarkSerializer(serializers.ModelSerializer):

    eqtype = TypeSerializer()

    class Meta:
        model = EqMark
        fields = ['id', 'eqmark', 'eqtype', 'eqmodel', 'manufacturer']