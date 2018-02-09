from django.test import TestCase, Client
from file_manager.models import Asset, Folder, Collection, Contributor, CountryTag, ContinentTagGroup, Tag, TagGroup
from api.serializers import AssetSerializer, CollectionSerializer, ContributorSerializer, CountryTagSerializer, TagSerializer,TagGroupSerializer
from django.conf import settings
from django.core.urlresolvers import reverse
from random import randint

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )

# Create your tests here.

class EndpointTests(TestCase):
    # Number of dummy assets to create
    dummy_count = 50
    small_dummy_count = 10
    # ----------- Set up ----------- #
    def setUp(self):
        client = Client()
        f = Folder(name='f')
        f.save()
        for i in range (0,self.small_dummy_count):
            Collection.objects.create(id=i, name="collection%d" % i)
            TagGroup.objects.create(id=i, name="tag-group%d" % i)
            ContinentTagGroup.objects.create(id=i, name="continent%d" % i)

        for i in range(0, self.dummy_count):
            taggroup = TagGroup.objects.filter(id=randint(0,self.small_dummy_count-1))[0]
            Tag.objects.create(id=i, name="tag%d" % i, group=taggroup)
            continent = ContinentTagGroup.objects.filter(id=randint(0,self.small_dummy_count-1))[0]
            CountryTag.objects.create(id=i, name="country%d" % i, continent=continent)
            Asset.objects.create(
                id=i, name="asset%d" % i, 
                parent=f, 
                collections=[randint(0,self.small_dummy_count-1)], 
                tags=[randint(0,self.small_dummy_count-1)] 
            )
            Contributor.objects.create(id=i, name="contributor%d" % i,)  

    # ----------- Tests ------------ #
    # ––––––– Core endpoints ––––––– #
    def test_assets(self):
        url = reverse('api:asset-list')

        # get API response
        response = self.client.get(url)
        # get db data
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_collections(self):
        url = reverse('api:collection-list')

        # get API response
        response = self.client.get(url)
        # get db data
        collections = Collection.objects.all()
        serializer = CollectionSerializer(collections, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_contributors(self):
        url = reverse('api:contributor-list')

        # get API response
        response = self.client.get(url)
        # get db data
        contributors = Contributor.objects.all()
        serializer = ContributorSerializer(contributors, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_countries(self):
        url = reverse('api:countrytag-list')

        # get API response
        response = self.client.get(url)
        # get db data
        countries = CountryTag.objects.all()
        serializer = CountryTagSerializer(countries, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_tags(self):
        url = reverse('api:tag-list')

        # get API response
        response = self.client.get(url)
        # get db data
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_tag_groups(self):
        url = reverse('api:taggroup-list')

        # get API response
        response = self.client.get(url)
        # get db data
        tag_groups = TagGroup.objects.all()
        serializer = TagGroupSerializer(tag_groups, many=True)
        self.assertEqual(response.data, serializer.data)

    # ––––––– Relation endpoints ––––––– #
    def test_asset_collection(self):
        # Check through collections making sure they contain the correct assets
        for i in range(0,self.small_dummy_count):
            # get db data
            assets = Asset.objects.filter(collections=i)
            # get API data
            url = reverse('api:asset-collection-list', args=[i])
            response = self.client.get(url)
            serializer = AssetSerializer(assets, many=True)
            self.assertEqual(response.data, serializer.data)

    def test_asset_tag(self):
        # Check through collections making sure they contain the correct assets
        for i in range(0,self.small_dummy_count):
            # get db data
            assets = Asset.objects.filter(tags=i)
            # get API data
            url = reverse('api:asset-tag-list', args=[i])
            response = self.client.get(url)
            serializer = AssetSerializer(assets, many=True)
            self.assertEqual(response.data, serializer.data)

    def test_asset_collection_tag(self):
        # Check through collections making sure they contain the correct assets
        for collection_id in range(0,self.small_dummy_count):
            for tag_id in (range(0, self.small_dummy_count)):
                # get db data
                assets = Asset.objects.filter(collections=collection_id).filter(tags=tag_id)
                # get API data
                url = reverse('api:asset-collection-tag-list', args=[collection_id,tag_id])
                response = self.client.get(url)
                serializer = AssetSerializer(assets, many=True)
                self.assertEqual(response.data, serializer.data)

    def test_asset_collection_location(self):
        # Check through collections making sure they contain the correct assets
        for collection_id in range(0,self.small_dummy_count):
            for country_id in (range(0, self.small_dummy_count)):
                # get db data
                assets = Asset.objects.filter(collections=collection_id).filter(locations=country_id)
                # get API data
                url = reverse('api:asset-collection-location-list', args=[collection_id,country_id])
                response = self.client.get(url)
                serializer = AssetSerializer(assets, many=True)
                self.assertEqual(response.data, serializer.data)