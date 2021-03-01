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
        marks = EqMark.objects.all()
        choosen, best_indices, add = choose_pumps(marks, (wpq, wph))
        srl = MarkSerializer(choosen, many=True)
        self.convert_points_to_float(srl.data)
        self.fill_with_additional_data(srl.data, add)
        data = {
            'all': srl.data,
            'best': best_indices,
        }
        return Response(data)

    def convert_points_to_float(self, data):
        for key in MarkSerializer.Meta.point_fields:
            for mark_data in data:
                mark_data[key] = get_list_points(mark_data[key])
        return data

    def fill_with_additional_data(self, data, add):
        for mark_data in data:
            _id = mark_data['id']
            mark_data.update(add[_id])
        return data

@api_view(['POST', 'GET'])
def init_select(request):
    column_names = [
        'Бренд',
        'Модель',
        'DN',
        'Стоимость',
        'Скорость',
        'Q/Qопт',
        'КПД',
        'Мощность',
        'на',
        'валу',
        'Расход',
        'Напор',
        'NPSH'
    ]
    indextokey = {
        0: 'eqtype-eqmodel-manufacturer-name',
        1: 'eqtype-eqmodel-eqmodel',
        2: 'dn',
        3: 'cost',
        4: 'speed',
        5: 'q_ratio',
        6: 'eff_wp',
        7: 'p2_wp',
        8: 'q_wp',
        9: 'h_wp',
        10: 'npsh_wp',
    }

    list_indextokey = {
        0: 'eqtype-eqmodel-manufacturer-name',
        1: 'eqtype-eqmodel-eqmodel',
    }

    best_indextokey = {
        0: 'eqtype-eqmodel-manufacturer-name',
        1: 'eqtype-eqmodel-eqmodel',
        2: 'eqmark',
        3: 'eqmark',
        4: 'eqmark',
        5: 'eqmark',
        6: 'eqmark',
        7: 'eqmark',
    }
    return Response({'indextokey': indextokey, 'list_indextokey': list_indextokey, 'best_indextokey': best_indextokey})
