from itertools import chain

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from file_manager.models import Asset, AssetLearnerJourney, Contributor, Collection, CountryTag, LearnerJourney, Tag, TagGroup
from . import serializers

# Create your views here.
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

class AssetPerLearnerJourneyViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Returns all Assets from a given Learner Journey
        """
        learner_journey_id = self.kwargs['id']
        asset_learner_journeys = AssetLearnerJourney.objects.filter(
            learner_journey=learner_journey_id).order_by('position')
        asset_query_sets = []
        for asset_learner_journey in asset_learner_journeys:
            asset_query_set = Asset.objects.get(id=asset_learner_journey.asset.id)
            asset_query_sets.append(asset_query_set)

        return list(chain(asset_query_sets))

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

class AssetPerCollectionAndLocationViewSet(ModelViewSet):
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

class LearnerJourneyViewSet(ModelViewSet):
    serializer_class = serializers.LearnerJourneySerializer
    queryset = LearnerJourney.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagGroupViewSet(ModelViewSet):
    serializer_class = serializers.TagGroupSerializer
    queryset = TagGroup.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
