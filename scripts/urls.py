from django.urls import path
from .views import UseCaseListCreateView, KeywordsListView, NetworkKeywordCreateView, ScriptInfoListView, ScriptInfoCreateView, ExecuteScriptView,  NetworkDeviceLogListCreateAPIView, NetworkDeviceLogRetrieveAPIView, NetworkDeviceInfoCreateAPIView, NetworkDeviceInfoListView, NetworkDeviceInfoDetailView, NetworkDeviceLogCreateAPIView

urlpatterns = [
    path('use-cases/', UseCaseListCreateView.as_view(), name='use-case-list-create'),
    path('network-devices/', NetworkDeviceInfoCreateAPIView.as_view(), name='network-device-create'),
    path('network-devices/list/', NetworkDeviceInfoListView.as_view(), name='network-device-list'),
    path('network-devices/<int:pk>/', NetworkDeviceInfoDetailView.as_view(), name='network-device-detail'),
    path('logs/create/', NetworkDeviceLogCreateAPIView.as_view(), name='networkdevice-log-create'),
    path('logs/', NetworkDeviceLogListCreateAPIView.as_view(), name='networkdevice-log-list'),
    path('logs/<int:pk>/', NetworkDeviceLogRetrieveAPIView.as_view(), name='networkdevice-log-detail'),
    path('execute/', ExecuteScriptView.as_view(), name='execute-script'),
    path('script-list/', ScriptInfoListView.as_view(), name='script-list'),
    path('create-script/', ScriptInfoCreateView.as_view(), name='script-create'),
    path('script-info/', NetworkKeywordCreateView.as_view(), name='script-info'),
    path('keyword-lists/', KeywordsListView.as_view(), name='keyword-lists'),

]

