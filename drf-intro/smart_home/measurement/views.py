# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from measurement.models import Sensor, Measurement
from measurement.serializers import SensorListSerializer, SensorSerializer, MeasurementListSerializer


class APISensorsView(ListCreateAPIView):

    queryset = Sensor.objects.all()
    serializer_class = SensorListSerializer


class APISensorDetailView(RetrieveUpdateAPIView):

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class APIMeasurementView(CreateAPIView):

    queryset = Measurement.objects.all()
    serializer_class = MeasurementListSerializer
