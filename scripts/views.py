from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScriptInfo, NetworkDeviceInfo, NetworkDeviceLog
from .serializers import ScriptInfoSerializer, ExecuteScriptSerializer, NetworkDeviceInfoSerializer, NetworkDeviceLogSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import generics
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import NetworkKeywordSerializer
from .models import NetworkKeyword

class NetworkKeywordCreateView(APIView):
    serializer_class = NetworkKeywordSerializer
    def post(self, request, format=None):
        # Deserialize the request data using the serializer
        serializer = NetworkKeywordSerializer(data=request.data, many=True)
        
        if serializer.is_valid():
            # Save the deserialized data to create multiple instances
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScriptInfoCreateView(APIView):
    serializer_class = ScriptInfoSerializer
    def post(self, request, format=None):
        serializer = ScriptInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScriptInfoListView(generics.ListAPIView):
    queryset = ScriptInfo.objects.all()
    serializer_class = ScriptInfoSerializer

class KeywordsListView(generics.ListAPIView):
    queryset = NetworkKeyword.objects.all()
    serializer_class = NetworkKeywordSerializer

class ExecuteScriptView(APIView):
    serializer_class = ExecuteScriptSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'script_room',
                openapi.IN_QUERY,
                description='The room for script execution',
                type=openapi.TYPE_STRING,
            ),
        ],
        request_body=ExecuteScriptSerializer,  # Use the serializer class
    )
    def post(self, request):
        serializer = ExecuteScriptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        script_room = serializer.validated_data['script_room']

        message = {
            'type': 'execute_script',
            'script_room': script_room,
        }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)('scripts', message)
        return Response({'message': 'Script execution initiated'}, status=status.HTTP_202_ACCEPTED)


class NetworkDeviceLogCreateAPIView(APIView):
    serializer_class = NetworkDeviceLogSerializer

    def post(self, request, format=None):
        # Get the device_ip from request.data
        device_ip = request.data.get('device_ip')
        print(device_ip)
        print(request.data)
        # Retrieve the device object using the device_ip
        try:
            device = NetworkDeviceInfo.objects.get(ip_address=device_ip)
        except Device.DoesNotExist:
            return Response({"error": f"Device with IP {device_ip} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Add the device to the request data
        request.data['device'] = device.id

        # Serialize the data with the updated request data
        serializer = NetworkDeviceLogSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class ExecuteScriptView(APIView):
#    def post(self, request, script_room):
#        message = {
#            'type': 'execute_script',
#            'script_room': script_room,
#        }
#        channel_layer = get_channel_layer()
#        async_to_sync(channel_layer.send)('scripts', message)
#        return Response({'message': 'Script execution initiated'}, status=status.HTTP_202_ACCEPTED)

#class NetworkDeviceLogCreateAPIView(APIView):
#    serializer_class = NetworkDeviceLogSerializer
#    def post(self, request, format=None):
#        serializer = NetworkDeviceLogSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NetworkDeviceLogListCreateAPIView(generics.ListCreateAPIView):
    queryset = NetworkDeviceLog.objects.all()
    serializer_class = NetworkDeviceLogSerializer

class NetworkDeviceLogRetrieveAPIView(generics.RetrieveAPIView):
    queryset = NetworkDeviceLog.objects.all()
    serializer_class = NetworkDeviceLogSerializer
    lookup_field = 'pk'  # Use 'pk' (primary key) for retrieving by ID
    
class NetworkDeviceInfoCreateAPIView(APIView):
    serializer_class = NetworkDeviceInfoSerializer
    def post(self, request, format=None):
        serializer = NetworkDeviceInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NetworkDeviceInfoListView(ListAPIView):
    queryset = NetworkDeviceInfo.objects.all()
    serializer_class = NetworkDeviceInfoSerializer

class NetworkDeviceInfoDetailView(RetrieveAPIView):
    queryset = NetworkDeviceInfo.objects.all()
    serializer_class = NetworkDeviceInfoSerializer
