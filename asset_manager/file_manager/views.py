from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Asset, Contributor, Collection, CountryTag, Tag, TagGroup
from . import serializers

# Create your views here.

def index(request):
    return render(request, 'file_manager/index.html')

class AssetViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class AssetPerCollectionViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['id']
        return Asset.objects.filter(collections__id=collection_id)

class AssetPerTagViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        tag_id = self.kwargs['id']
        return Asset.objects.filter(tags__id=tag_id)

class AssetPerCollectionAndTagViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        tag_id = self.kwargs['tag_id']
        return Asset.objects.filter(collections__id=collection_id).filter(tags__id=tag_id)

class AssetPerCollectionAndCountryViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        location_id = self.kwargs['location_id']
        return Asset.objects.filter(collections__id=collection_id).filter(locations__id=location_id)

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
