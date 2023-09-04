from rest_framework import serializers
from .models import NetworkDeviceInfo, NetworkDeviceLog

class ExecuteScriptSerializer(serializers.Serializer):
    script_room = serializers.CharField()

class NetworkDeviceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkDeviceInfo
        fields = ('id', 'status', 'ip_address', 'host_name', 'info')

class NetworkDeviceLogSerializer(serializers.ModelSerializer):
    device_ip = serializers.CharField(source='device.ip_address', read_only=True)

    class Meta:
        model = NetworkDeviceLog
        fields = ['device_id', 'device_ip', 'log_data', 'created_at']
#class NetworkDeviceLogSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = NetworkDeviceLog
#        fields = '__all__'
