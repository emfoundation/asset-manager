from itertools import chain

from django.shortcuts import render
from django.db.models import Count
from django.db.models import F

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from file_manager.models import Answer, Asset, Chapter, Contributor, Collection, CountryTag, LearnerJourney, Question, Tag, TagGroup
from . import serializers

# Create your views here.
class AnswerViewSet(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class AnswerPerCollectionAndQuestionViewSet(ModelViewSet):
    serializer_class = serializers.AnswerPlusFormatSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        question_id = self.kwargs['question_id']
        return Answer.objects.filter(
            question=question_id).filter(
            asset__collections=collection_id).annotate(
            format=F('asset__format')).order_by('position')

class AssetViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class AssetPerAnswerViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        answer_id = self.kwargs['answer_id']
        asset = Answer.objects.get(id=answer_id).asset
        return [asset]

class AssetPerCollectionViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['id']
        return Asset.objects.filter(collections__id=collection_id)

class AssetPerCollectionAndLearnerJourneyViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        Returns all Assets from a given Learner Journey
        """
        learner_journey_id = self.kwargs['learner_journey_id']
        collection_id = self.kwargs['collection_id']
        chapters = Chapter.objects.filter(
            learner_journey=learner_journey_id).filter(asset__collections=collection_id).order_by('position')
        asset_query_sets = []
        for chapter in chapters:
            asset_query_set = Asset.objects.get(id=chapter.asset.id)
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

class AssetPerCollectionAndTagGroupViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        tag_group_id = self.kwargs['tag_group_id']

        tags = Tag.objects.filter(group=tag_group_id)
        return Asset.objects.filter(collections__id=collection_id).filter(tags__in=tags).distinct()

class AssetPerCollectionAndLocationViewSet(ModelViewSet):
    serializer_class = serializers.AssetSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        location_id = self.kwargs['location_id']
        return Asset.objects.filter(collections__id=collection_id).filter(locations__id=location_id)

class ChapterViewSet(ModelViewSet):
    serializer_class = serializers.ChapterSerializer
    queryset = Chapter.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

# class ChapterPlusAssetViewSet(ModelViewSet):
#     serializer_class = serializers.ChapterSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     def get_queryset(self):
#         collection_id = self.kwargs['collection_id']
#         learner_journey_id = self.kwargs['learner_journey_id']
#         chapter_num = int(self.kwargs['chapter_num'])
#         chapters = Chapter.objects.filter(learner_journey=learner_journey_id).filter(asset__collections=collection_id).order_by('position')
#         return [chapters[chapter_num -1]]

class ChapterPerCollectionAndLearnerJourneyViewSet(ModelViewSet):
    serializer_class = serializers.ChapterSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        learner_journey_id = self.kwargs['learner_journey_id']
        return Chapter.objects.filter(learner_journey=learner_journey_id).filter(asset__collections=collection_id).order_by('position')

class ChapterIdsPerCollectionAndLearnerJourneyViewSet(ModelViewSet):
    serializer_class = serializers.ChapterIdsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        collection_id = self.kwargs['collection_id']
        learner_journey_id = self.kwargs['learner_journey_id']
        return Chapter.objects.filter(learner_journey=learner_journey_id).filter(asset__collections=collection_id).order_by('position')

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

    def get_queryset(self):
        return LearnerJourney.objects.annotate(parts=Count('chapter'))

class QuestionViewSet(ModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagViewSet(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

class TagGroupViewSet(ModelViewSet):
    serializer_class = serializers.TagGroupSerializer
    queryset = TagGroup.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
