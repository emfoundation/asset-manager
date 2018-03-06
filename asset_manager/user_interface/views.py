from django.shortcuts import render
from file_manager.models import TagGroup, Tag, Asset
from django.conf import settings

formatToIcon = {
	'IM': 'image',
	'VI': 'video',
	'PR': 'file-powerpoint',
	'LN': 'link',
	'AU': 'headphones',
	'DO': 'file',
	'OT': 'file'
}

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
		'assets': assets,
		'formatToIcon': formatToIcon
	}
	return render(request, 'user_interface/topic.html', context)

def asset(request, asset_id):
	item = Asset.objects.get(id=asset_id)
	filename = ('https://' + settings.AWS_STORAGE_BUCKET_NAME
		+ '.s3.amazonaws.com/media/' + item.file.name)
	topicGroup = request.GET.get('t', '')
	icon = formatToIcon.get(item.format, 'OT')
	context = { 
		'asset': item,
		'filename': filename,
		'topicGroup': topicGroup,
		'icon': icon
	}
	return render(request, 'user_interface/asset.html', context)