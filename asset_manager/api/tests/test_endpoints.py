from django.test import TestCase
from file_manager.models import Asset, Folder
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIRequestFactory, RequestsClient
from asset_manager import urls

import logging
logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format=' %(asctime)s - %(levelname)s - %(message)s'
    )
# Create your tests here.

class EndpointTests(TestCase):

    factory = APIRequestFactory()

    # ----------- Set up ----------- #
    def setUp(self):
        f = Folder(name='f')
        f.save()
        for i in range(1, 10):
            Asset.objects.create(name="asset%d" % i, parent=f)

    # ----------- Tests ------------ #

    def test_assets(self):
        url = reverse('api:assets')
        response = self.client.get('/api/assets/')
        print(response.content)
        print(url)
        # self.assertEqual(response.content, Asset.objects.all())
