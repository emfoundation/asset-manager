from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Asset
from .serializers import AssetSerializer

# Create your views here.
class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
