from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NetworkDeviceInfo, NetworkDeviceLog
from .serializers import NetworkDeviceInfoSerializer, NetworkDeviceLogSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import generics

class NetworkDeviceLogCreateAPIView(APIView):
    serializer_class = NetworkDeviceLogSerializer
    def post(self, request, format=None):
        serializer = NetworkDeviceLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
