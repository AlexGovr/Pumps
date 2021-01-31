import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Manufacturer, EqMark, EqModel, EqType
from .serializers import ManufacturerSerializer, EqModelSerializer
from .serializers import TypeSerializer, MarkSerializer
from .plots import choose_pumps


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

    @action(detail=False, url_path='select', methods=['post'])
    def select(self, request):
        print(request.data['parameters'])
        data =json.loads(request.data['parameters'])
        print(data)
        wpq = int(data['wpq'])
        wph = int(data['wph'])
        eqtype_name = data['eqtype']
        marks = EqMark.objects.filter(eqtype=EqType.objects.get(eqtype=eqtype_name))
        choosen = choose_pumps(marks, (wpq, wph))
        srl = MarkSerializer(choosen, many=True)
        print('here')
        # srl.data['success'] = True
        r = Response(srl.data)
        return Response(srl.data)