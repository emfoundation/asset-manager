from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Asset, Contributor, Collection, CountryTag, Tag, TagGroup
from . import serializers

# Create your views here.
class AssetViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class ContributorViewSet(ModelViewSet):
    serializer_class = serializers.ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class CollectionViewSet(ModelViewSet):
    serializer_class = serializers.CollectionSerializer
    queryset = Collection.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class CountryTagViewSet(ModelViewSet):
    serializer_class = serializers.CountryTagSerializer
    queryset = CountryTag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagGroupViewSet(ModelViewSet):
    serializer_class = serializers.TagGroupSerializer
    queryset = TagGroup.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
