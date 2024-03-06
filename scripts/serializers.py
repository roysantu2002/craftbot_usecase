from rest_framework import serializers
from .models import NetworkDeviceInfo, NetworkDeviceLog, ScriptInfo, NetworkKeyword
from .models import UseCase, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UseCaseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)

    class Meta:
        model = UseCase
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data:
            category_instance = Category.objects.create(**category_data)
            validated_data['category'] = category_instance
        return super(UseCaseSerializer, self).create(validated_data)
    
class ScriptInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptInfo
        fields = '__all__'

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
        fields = ['device', 'device_ip', 'log_data', 'created_at']
#class NetworkDeviceLogSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = NetworkDeviceLog
#        fields = '__all__'

class NetworkKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkKeyword
        fields = '__all__'
