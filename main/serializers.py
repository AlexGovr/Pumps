
from rest_framework import serializers
from .models import Manufacturer, EqMark, EqModel, EqType


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['name', 'id']


class EqModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EqModel
        fields = ['id', 'eqmodel', 'manufacturer']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EqType
        fields = ['id', 'eqtype', 'eqmodel', 'manufacturer']


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EqMark
        fields = ['id', 'eqmark', 'eqtype', 'eqmodel', 'manufacturer']