# import time as t
# from selenium import webdriver
# import pytest
#
#
# @pytest.fixture
# def background():
#
#    global driver
#
#    driver = webdriver.Remote(
#      command_executor='https://hub.propertyfinder.nt/wd/hub',
#      desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})
#    driver.get("https://staging.propertyfinder.ae")
#    yield
#    driver.close()
#    driver.quit()
#
#
# @pytest.mark.usefixtures('background')
# class TestClass:
#
#     def test_demo(self):
#         driver.find_elements_by_css_selector('[class="featured-properties__detail"]')[0].click()
#         t.sleep(5)
