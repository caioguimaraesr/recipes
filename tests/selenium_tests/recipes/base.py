from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
