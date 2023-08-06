# from selenium import webdriver
# import pytest
# from pytest_html_reporter import attach
#
# global driver
#
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# # def pytest_runtest_makereport(item, call):
# #     breakpoint()
# #     outcome = yield
# #     attach(data=driver.get_screenshot_as_png(), name='screenshot1')
# #
# #     rep = outcome.get_result()
# #     setattr(item, "rep_" + rep.when, rep)
# #     return rep
#
#
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
#
#
#
# def test_demo():
#     driver = webdriver.Chrome()
#
#     driver.get("http://www.python.org")
#     driver.find_elements_by_css_selector('[class="featured-properties__detail"]')[0].click()
#     driver.close()
#     driver.quit()
#     # attach(data=driver.get_screenshot_as_png(), name='screenshot1')
#
#
# import pytest
#
#
# def track_test_fails():
#     @pytest.mark.tryfirst
#     def pytest_runtest_makereport(item, call, __multicall__):
#         # execute all other hooks to obtain the report object
#         rep = __multicall__.execute()
#         # `when` is setup, call, teardown
#         setattr(item, "rep_" + rep.when, rep)
#
#         # mark failures explicitly
#         if hasattr(item, 'rep_setup') and hasattr(item, 'rep_call'):
#             item.test_failed = (
#                 item.rep_setup.passed and item.rep_call.failed
#             )
#
#         return rep
#
#     return pytest_runtest_makereport
#
#
# pytest_runtest_makereport = track_test_fails()
#
#
# @pytest.yield_fixture
# def foo(request):
#     yield
#
#     if request.node.test_failed:
#         pytest.fail(
#             "Maybe your test failed because X, Y, Z or you can skip with ..."
#         )
#
#
# def test_foo(foo):
#     assert False
#
#
# from selenium import webdriver
# import pytest
# from pytest_html_reporter import attach
#
#
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# # def pytest_runtest_makereport(__multicall__):
# #     report = __multicall__.execute()
# #     breakpoint()
# #     if report.when == 'call':
# #         xfail = hasattr(report, 'wasxfail')
# #         if (report.skipped and xfail) or (report.failed and not xfail):
# #             try:
# #                 attach(data=driver.get_screenshot_as_png(), name='screenshot1')
# #             except Exception as e:
# #                 print("Error saving screenshot !!")
# #
# #     return report
#
# # def tear_down(request):
# #     method_name = request.node.name
# #     breakpoint()
# #     attach(data=driver.get_screenshot_as_png(), name='screenshot1')
# #     # if request.node.rep_call.failed:
# #     #     print('test {} failed :('.format(method_name))
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item, call):
#     breakpoint()
#     outcome = yield
#     rep = outcome.get_result()
#     setattr(item, "rep_" + rep.when, rep)
#     return rep
#
# @pytest.fixture
# def background():
#     global driver
#
#     driver = webdriver.Chrome()
#     driver.get("http://www.python.org")
#     yield
#     driver.close()
#     driver.quit()
#
#
# # @pytest.fixture
# # def tear_down(request):
# #     method_name = request.node.name
# #     if request.node.rep_call.failed:
# #         print('test {} failed :('.format(method_name))
#
# @pytest.mark.usefixtures('background')
# class TestClass:
#
#     def test_demo(self):
#         driver.find_elements_by_css_selector('[class="featured-properties__detail"]')[0].click()
#         # attach(data=driver.get_screenshot_as_png(), name='screenshot1')
#
#
#
# import pytest
# from selenium import webdriver
#
#
# # @pytest.mark.tryfirst
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# # @pytest.mark.hookwrapper
# # def pytest_runtest_makereport(item, call, __multicall__):  # @UnusedVariable
# #     breakpoint()
# #     rep = __multicall__.execute()
# #     setattr(item, "rep_" + rep.when, rep)
# #     return rep
# #
# #
# # @pytest.yield_fixture(scope='function')
# # def foo():
# #     global driver
# #     driver = webdriver.Chrome()
# #     driver.get("http://www.python.org")
# #
# #     yield
# #
# #     driver.close()
# #     driver.quit()
#
#
# @pytest.mark.usefixtures("setup")
# def test_title(self):
#     assert "Selenium Easy" in self.driver.title
#
# # @pytest.mark.usefixtures("setup")
# # def test_foo(self):
# #     self.driver.find_elements_by_css_selector('[class="featured-properties__detail"]')[0].click()
