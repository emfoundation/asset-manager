from rest_framework import serializers
from file_manager import models

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('__all__')

class AnswerPlusFormatSerializer(serializers.ModelSerializer):
    format = serializers.CharField()
    class Meta:
        model = models.Answer
        fields = ('id', 'title', 'tile_description', 'question_context', 'description', 'asset', 'question', 'position', 'thumbnail', 'format',)

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = ('id', 'name', 'file', 'link', 'description', 'duration', \
            'creation_date', 'copyright_info', 'enabled', 'status', \
            'type_field', 'filetype', 'uploaded_at', 'last_edit_at', \
            'tags', 'locations', 'contributors', 'collections', )

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ('__all__')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ('id', 'name', )

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ('id', 'name', )

class CountryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CountryTag
        fields = ('id', 'name', 'display_name', 'code',)

class LearnerJourneySerializer(serializers.ModelSerializer):
    parts = serializers.IntegerField()
    class Meta:
        model = models.LearnerJourney
        fields = ('id', 'name', 'description', 'parts', 'duration', 'thumbnail')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('__all__')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'group', 'deprecated', )

class TagGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagGroup
        fields = ('id', 'name', )
