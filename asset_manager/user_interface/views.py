from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg
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

# very brittle: we should consider creating a field on TagGroup to hold the svg file
tagGroupToIcon = {
	'BIOCYCLE': 'bug',
	'BUILT ENVIRONMENT': 'building',
	'BUSINESS': 'briefcase',
	'DESIGN': 'brush',
	'ECONOMICS': 'pie-chart',
	'EDUCATION (LEARNING)': 'map',
	'ENERGY': 'lightning',
	'FINANCE & LEGAL': 'balance',
	'GOVERNMENT': 'bank',
	'MANUFACTURING & ENGINEERING': 'idea',
	'MATERIALS': 'lab',
	'TECHNICAL CYCLE': 'gears',
	'TECHNOLOGY': 'touch'
}

# Create your views here.
def index(request):
	topics = TagGroup.objects.all()
	context = { 
		'topics': topics,
		'tagGroupToIcon': tagGroupToIcon
	}
	return render(request, 'user_interface/index.html', context)

def topic(request, topic_id):
	thisTopic = TagGroup.objects.get(id=topic_id)
	tags = Tag.objects.filter(group__id=topic_id)
	assets = Asset.objects.filter(tags__in=tags).distinct()
	typeChoices = { k:v for (k,v) in Asset.TYPE_CHOICES }

	context = { 
		'topic': thisTopic,
		'assets': assets,
		'formatToIcon': formatToIcon,
		'typeChoices': typeChoices
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

def search(request):
	searchTerm = request.GET.get('q', '')

	if searchTerm:
		queries = [SearchQuery(term) for term in searchTerm.split(' ')]
		query = queries.pop()
		for item in queries:
			query &= item

		vector = (
			SearchVector('name', weight='A') +
			SearchVector('description', weight='A') +
			SearchVector(StringAgg('tags__name', delimiter=' '), weight='B') +
			SearchVector(StringAgg('locations__name', delimiter=' '), weight='B') +
			SearchVector(StringAgg('contributors__name', delimiter=' '), weight='B')
		)
		
		assets = Asset.objects.annotate(document=vector, rank=SearchRank(vector, query))\
					  .filter(document=query).order_by('type_field', '-rank')
	else:
		assets = None
	typeChoices = { k:v for (k,v) in Asset.TYPE_CHOICES }

	context = { 
		'searchTerm': searchTerm,
		'assets': assets,
		'formatToIcon': formatToIcon,
		'typeChoices': typeChoices
	}

	return render(request, 'user_interface/search.html', context)

def data(request):
   return render(request, 'data.html')
