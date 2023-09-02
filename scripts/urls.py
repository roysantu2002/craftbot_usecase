from django.urls import path
from .views import NetworkDeviceInfoCreateAPIView, NetworkDeviceInfoListView, NetworkDeviceInfoDetailView

urlpatterns = [
    path('api/network-devices/', NetworkDeviceInfoCreateAPIView.as_view(), name='network-device-create'),
    path('api/network-devices/list/', NetworkDeviceInfoListView.as_view(), name='network-device-list'),
    path('api/network-devices/<int:pk>/', NetworkDeviceInfoDetailView.as_view(), name='network-device-detail'),
]

