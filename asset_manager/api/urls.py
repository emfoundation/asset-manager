from rest_framework.routers import SimpleRouter
from . import views
from file_manager import models

router = SimpleRouter()

router.register("assets/tag/(?P<id>\d+)", views.AssetPerTagViewSet, 'asset')
router.register("assets/collection/(?P<collection_id>\d+)/tag/(?P<tag_id>\d+)",
		views.AssetPerCollectionAndTagViewSet, 'asset')
router.register("assets", views.AssetViewSet)
router.register("collections", views.CollectionViewSet)
router.register("contributors", views.ContributorViewSet)
router.register("countries", views.CountryTagViewSet)
router.register("tags", views.TagViewSet)
router.register("tag-groups", views.TagGroupViewSet)

urlpatterns = router.urls
