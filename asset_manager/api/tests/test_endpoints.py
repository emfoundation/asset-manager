from django.test import TestCase, Client
from file_manager.models import Asset, Folder, Collection, Contributor
from api.serializers import AssetSerializer, CollectionSerializer, ContributorSerializer
from django.conf import settings
from django.core.urlresolvers import reverse
from random import randint
# from rest_framework.test import APIClient
# from api import urls

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# Create your tests here.

class EndpointTests(TestCase):

    # ----------- Set up ----------- #
    def setUp(self):
        client = Client()

        f = Folder(name='f')
        f.save()
        for i in range (0,5):
            Collection.objects.create(id=i, name="collection%d" % i)

        for i in range(0, 50):
            Asset.objects.create(id=i, name="asset%d" % i, parent=f, collections=[randint(0,4)] )
            Contributor.objects.create(id=i, name="contributor%d" % i,)
            

    # ----------- Tests ------------ #

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
