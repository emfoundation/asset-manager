"""asset_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from file_manager import views

router = SimpleRouter()
# "assets" defines the url pattern ie localhost:8000/assets/
router.register("api/assets/tag/(?P<id>\d+)", views.AssetPerTagViewSet, 'asset')
router.register("api/assets/collection/(?P<collection_id>\d+)/tag/(?P<tag_id>\d+)", 
		views.AssetPerCollectionAndTagViewSet, 'asset')
router.register("api/assets/collection/(?P<collection_id>\d+)/country/(?P<country_id>\d+)", 
		views.AssetPerCollectionAndCountryViewSet, 'asset')
router.register("api/assets", views.AssetViewSet)
router.register("api/collections", views.CollectionViewSet)
router.register("api/contributors", views.ContributorViewSet)
router.register("api/countries", views.CountryTagViewSet)
router.register("api/tags", views.TagViewSet)
router.register("api/tag-groups", views.TagGroupViewSet)

urlpatterns = router.urls + [
    url(r'^admin/', admin.site.urls),
    url(r'^jwt-auth/', obtain_jwt_token),
]
