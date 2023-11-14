from django.urls import path

from measurement.views import APISensorsView, APISensorDetailView, APIMeasurementView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', APISensorsView.as_view()),
    path('sensors/<int:pk>/', APISensorDetailView.as_view()),
    path('measurements/', APIMeasurementView.as_view()),
]
