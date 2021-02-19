import json
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Manufacturer, EqMark, EqModel, EqType
from .serializers import ManufacturerSerializer, EqModelSerializer
from .serializers import TypeSerializer, MarkSerializer
from .plots import choose_pumps, get_list_points


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
        data =json.loads(request.data['parameters'])
        wpq = float(data['wpq'])
        wph = float(data['wph'])
        eqtype_name = data['eqtype']
        marks = EqMark.objects.filter(eqtype=EqType.objects.get(eqtype=eqtype_name))
        choosen = choose_pumps(marks, (wpq, wph))
        srl = MarkSerializer(choosen, many=True)
        self.convert_points_to_float(srl.data)
        return Response(srl.data)

    def convert_points_to_float(self, data):
        for key in MarkSerializer.Meta.point_fields:
            for mark_data in data:
                mark_data[key] = get_list_points(mark_data[key])

@api_view(['POST', 'GET'])
def init_select(request):
    column_names = [

    ]
    indextokey = {
        0: 'eqtype-eqmodel-manufacturer-name',
        1: 'eqtype-eqmodel-eqmodel',
        2: 'eqmark',
        3: 'eqmark',
        4: 'eqmark',
        5: 'eqmark',
        6: 'eqmark',
        7: 'eqmark',
        8: 'eqmark',
        9: 'eqmark',
    }
    list_indextokey = {
        0: 'eqtype-eqmodel-manufacturer-name',
        1: 'eqtype-eqmodel-eqmodel',
    }
    return Response({'indextokey': indextokey, 'list_indextokey': list_indextokey})


# class InitPage(APIView):

#     def get()