# import time as t
# from selenium import webdriver
# import pytest
# from pytest_html_reporter import attach
#
# k = 0
#
# @pytest.fixture
# def background():
#
#     global driver, k
#     #
#     # if k == 0:
#     #     driver = webdriver.Chrome()
#     #     driver.get("http://www.python.org")
#     #     yield
#     #     driver.close()
#     #     driver.quit()
#     #     k += 1
#     # else:
#     #     driver = webdriver.Remote(
#     #         command_executor='https://0.0.0.0:8080/wd/hub',
#     #         desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})
#     #     driver.get("https://staging.propertyfinder.ae")
#     #     yield
#     #     driver.close()
#     #     driver.quit()
#
#     # if k != 0:
#     driver = webdriver.Chrome()
#     driver.get("http://www.python.org")
#     # driver = webdriver.Remote(
#     #     command_executor='https://0.0.0.0:8080/wd/hub',
#     #     desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})
#     # driver.get("https://google.ae")
#     yield
#     driver.close()
#     driver.quit()
#     # else:
#     #     k += 1
#     #     driver = webdriver.Remote(
#     #      command_executor='https://0.0.0.0:8080/wd/hub',
#     #      desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True})
#     #     driver.get("https://staging.propertyfinder.ae")
#     #     yield
#     #     driver.close()
#     #     driver.quit()
#
#
# @pytest.mark.usefixtures('background')
# class TestClass:
#
#     def test_demo(self):
#         print('am here')
#         breakpoint()
#         driver.find_elements_by_css_selector('[class="featured-properties__detail"]')[0].click()
#         driver.save_screenshot('sd.png')
#         attach()
#
# # def test_pass():
# #     pass
# #
# #
# # def test_fail():
# #     raise Exception('fail')
