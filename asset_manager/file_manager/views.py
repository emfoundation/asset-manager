from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Asset
from .serializers import AssetSerializer

# Create your views here.
class AssetViewSet(ModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
