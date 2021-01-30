
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Manufacturer, EqMark, EqModel, EqType
from .serializers import ManufacturerSerializer, EqModelSerializer
from .serializers import TypeSerializer, MarkSerializer


class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = EqType.objects.all()
    serializer_class = TypeSerializer


class ModelViewSet(viewsets.ModelViewSet):
    queryset = EqModel.objects.all()
    serializer_class = EqModelSerializer


class MarkViewSet(viewsets.ModelViewSet):
    queryset = EqMark.objects.all()
    serializer_class = MarkSerializer