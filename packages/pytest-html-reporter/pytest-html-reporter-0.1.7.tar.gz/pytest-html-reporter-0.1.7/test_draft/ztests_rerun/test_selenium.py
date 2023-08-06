import time as t
from selenium import webdriver
import pytest


@pytest.fixture
def background():

   global driver

   driver = webdriver.Remote(
     command_executor='https://0.0.0.0:8080/wd/hub',
     desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})
   driver.get("https://google.ae")
   yield
   driver.close()
   driver.quit()


@pytest.mark.usefixtures('background')
class TestClass:

    def test_demo(self):
        driver.find_element_by_css_selector('[aria-label="Search"]').send_keys('Jesus is coming soon!')

    def test_demox2(self):
        driver.find_element_by_css_selector('[aria-label="Search"]').send_keys('Jesus is coming soon!')

def test_pass():
    pass


def test_fail():
    raise Exception('fail')