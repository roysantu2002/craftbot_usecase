from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import NetworkDeviceInfo
from .serializers import NetworkDeviceInfoSerializer, NetworkDeviceLogSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView

class NetworkDeviceLogCreateAPIView(APIView):
    serializer_class = NetworkDeviceLogSerializer
    def post(self, request, format=None):
        serializer = NetworkDeviceLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
