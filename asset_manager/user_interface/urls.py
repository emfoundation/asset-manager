from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^topic/(?P<topic_id>\d+)$', views.topic, name='topic'),
    url(r'^asset/(?P<asset_id>\d+)$', views.asset, name='asset'),
    url(r'^search$', views.search, name='search'),
    url(r'data/$', views.data, name='data'),
]
