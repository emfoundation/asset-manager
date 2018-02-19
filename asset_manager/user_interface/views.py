from django.shortcuts import render
from file_manager.models import TagGroup, Tag, Asset

# Create your views here.
def index(request):
    return render(request, 'user_interface/index.html')

def list(request):
	tagGroups = TagGroup.objects.all()
	context = { 'tagGroups': tagGroups }
	return render(request, 'user_interface/list.html', context)

def tag_group(request, tag_group_id):
	sub_tags = Tag.objects.filter(group__id=tag_group_id)
	assets = Asset.objects.filter(tags__in=sub_tags)
	context = { 'assets': assets }
	return render(request, 'user_interface/tag.html', context)
