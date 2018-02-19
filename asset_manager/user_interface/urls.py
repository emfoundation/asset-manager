from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list$', views.list, name='list'),
    url(r'^tag/(?P<tag_group_id>\d+)$', views.tag_group, name='tag-group'),
]
