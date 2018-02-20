from django.shortcuts import render
from file_manager.models import TagGroup, Tag, Asset
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'user_interface/index.html')

def list(request):
	tagGroups = TagGroup.objects.all()
	context = { 'tagGroups': tagGroups }
	return render(request, 'user_interface/list.html', context)

def tag_group(request, tag_group_id):
	tagGroup = TagGroup.objects.get(id=tag_group_id)
	subTags = Tag.objects.filter(group__id=tag_group_id)
	assets = Asset.objects.filter(tags__in=subTags)
	context = { 
		'tagGroup': tagGroup,
		'assets': assets
	}
	return render(request, 'user_interface/tag.html', context)

def asset(request, asset_id):
	item = Asset.objects.get(id=asset_id)
	context = { 
		'asset': item,
		'bucket': settings.AWS_STORAGE_BUCKET_NAME
	}
	return render(request, 'user_interface/asset.html', context)