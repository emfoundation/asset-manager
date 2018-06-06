from rest_framework.routers import SimpleRouter
from . import views
from file_manager import models

router = SimpleRouter()

router.register(
	"answers/collection/(?P<collection_id>\d+)/question/(?P<question_id>\d+)",
	views.AnswerPerCollectionAndQuestionViewSet,
	'answer-collection-question'
)
router.register(
	"asset/answer/(?P<answer_id>\d+)",
	views.AssetPerAnswerViewSet,
	'asset-answer'
)
router.register(
	"assets/collection/(?P<id>\d+)",
	views.AssetPerCollectionViewSet,
	'asset-collection'
	)
router.register(
	"assets/tag/(?P<id>\d+)",
	views.AssetPerTagViewSet,
	'asset-tag'
	)
router.register(
	"assets/collection/(?P<collection_id>\d+)/tag/(?P<tag_id>\d+)",
	views.AssetPerCollectionAndTagViewSet,
	'asset-collection-tag')
router.register(
	"assets/collection/(?P<collection_id>\d+)/tag-group/(?P<tag_group_id>\d+)",
	views.AssetPerCollectionAndTagGroupViewSet,
	'asset-collection-tag-group'
)
router.register(
	"assets/collection/(?P<collection_id>\d+)/location/(?P<location_id>\d+)",
	views.AssetPerCollectionAndLocationViewSet,
	'asset-collection-location'
),
router.register(
	"assets/collection/(?P<collection_id>\d+)/learner-journey/(?P<learner_journey_id>\d+)",
	views.AssetPerCollectionAndLearnerJourneyViewSet,
	'asset-collection-learner-journey'
),
router.register(
	"chapters/collection/(?P<collection_id>\d+)/learner-journey/(?P<learner_journey_id>\d+)",
	views.ChapterPerCollectionAndLearnerJourneyViewSet,
	'chapter-collection-learner-journey'
),
router.register(
	"chapter-ids/collection/(?P<collection_id>\d+)/learner-journey/(?P<learner_journey_id>\d+)",
	views.ChapterIdsPerCollectionAndLearnerJourneyViewSet,
	'chapter-ids-collection-learner-journey'
),
# router.register(
# 	"chapters/collection/(?P<collection_id>\d+)/learner-journey/(?P<learner_journey_id>\d+)/chapter/(?P<chapter_num>\d+)",
# 	views.ChapterPlusAssetViewSet,
# 	'chapter-plus-asset'
# )
router.register("answers", views.AnswerViewSet)
router.register("assets", views.AssetViewSet)
router.register("chapters", views.ChapterViewSet)
router.register("collections", views.CollectionViewSet)
router.register("contributors", views.ContributorViewSet)
router.register("countries", views.CountryTagViewSet)
router.register("learner-journeys", views.LearnerJourneyViewSet)
router.register("questions", views.QuestionViewSet)
router.register("tags", views.TagViewSet)
router.register("tag-groups", views.TagGroupViewSet)

urlpatterns = router.urls
