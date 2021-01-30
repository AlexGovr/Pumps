
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Manufacturer, EqMark, EqModel, EqType
from .serializers import ManufacturerSerializer, EqModelSerializer
from .serializers import TypeSerializer, MarkSerializer
from .plots import choose_pumps


class SelectViewSet(viewsets.ViewSet):
    queryset = EqMark.objects.none()

    @action(methods=['post'], detail=True, url_path='/post/')
    def select(request):
        data = request.data
        wpq = data['wpq']
        wph = data['wph']
        eqtype_name = data['eqtype']
        marks = EqMark.objects.filter(eqtype=EqType.objects.get(eqtype=eqtype_name))
        choosen = choose_pumps(marks, (wpq, wph))
        srl = MarkSerializer(choosen, many=True)
        print(srl.validated_data)
        return Response(srl.data)

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