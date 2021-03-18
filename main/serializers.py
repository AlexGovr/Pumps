
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
        fields = [
            'id', 'eqmark', 'eqtype',
            'eqmodel', 'manufacturer',
            'cost', 'speed', 'dn',
            'q_optimal', 'mass',
        ]
        curve_fields = [
            'h_curve_points',
            'q_curve_points',
            'p2_curve_points',
            'npsh_curve_points',
            'efficiency_curve_points',
        ]
        fields += curve_fields