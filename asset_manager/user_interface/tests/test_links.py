from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from django.test.utils import override_settings
from django.urls import reverse
from selenium.webdriver.firefox.webdriver import WebDriver

# Create your tests here.

class LinkTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super(LinkTestCase, self).setUp()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)

    def tearDown(self):
        self.selenium.quit()
        super(LinkTestCase, self).tearDown()

    @override_settings(DEBUG=True)
    def test_index(self):
        selenium = self.selenium
        # Open the index page
        selenium.get('%s%s' % (self.live_server_url, reverse('user_interface:index')))
        links = selenium.find_elements_by_tag_name('a')   
        
        for link in links:
            print("Link: %s" % link.get_attribute('href'))    
    
