from django.urls import path
from .views import  NetworkDeviceLogListCreateAPIView, NetworkDeviceLogRetrieveAPIView, NetworkDeviceInfoCreateAPIView, NetworkDeviceInfoListView, NetworkDeviceInfoDetailView, NetworkDeviceLogCreateAPIView

urlpatterns = [
    path('network-devices/', NetworkDeviceInfoCreateAPIView.as_view(), name='network-device-create'),
    path('network-devices/list/', NetworkDeviceInfoListView.as_view(), name='network-device-list'),
    path('network-devices/<int:pk>/', NetworkDeviceInfoDetailView.as_view(), name='network-device-detail'),
    path('logs/create/', NetworkDeviceLogCreateAPIView.as_view(), name='networkdevice-log-create'),
    path('logs/', NetworkDeviceLogListCreateAPIView.as_view(), name='networkdevice-log-list'),
    path('logs/<int:pk>/', NetworkDeviceLogRetrieveAPIView.as_view(), name='networkdevice-log-detail'),
]

