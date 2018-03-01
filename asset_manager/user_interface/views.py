from django.shortcuts import render
from file_manager.models import TagGroup, Tag, Asset
from django.conf import settings

# Create your views here.
def index(request):
	topics = TagGroup.objects.all()
	context = { 'topics': topics }
	return render(request, 'user_interface/index.html', context)

def topic(request, topic_id):
	thisTopic = TagGroup.objects.get(id=topic_id)
	tags = Tag.objects.filter(group__id=topic_id)
	assets = Asset.objects.filter(tags__in=tags).distinct()
	context = { 
		'topic': thisTopic,
		'assets': assets
	}
	return render(request, 'user_interface/topic.html', context)

def asset(request, asset_id):
	item = Asset.objects.get(id=asset_id)
	context = { 
		'asset': item,
		'bucket': settings.AWS_STORAGE_BUCKET_NAME
	}
	return render(request, 'user_interface/asset.html', context)