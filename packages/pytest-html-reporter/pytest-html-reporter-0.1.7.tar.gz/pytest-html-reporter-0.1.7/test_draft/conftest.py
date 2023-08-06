# import pytest
# from pytest_html_reporter import attach
#
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# # def pytest_runtest_makereport(item, call):
# #     outcome = yield
# #     rep = outcome.get_result()
# #     setattr(item, "rep_" + rep.when, rep)
# #     return rep
# #
# # @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# # def pytest_runtest_makereport(item, call):
# #     breakpoint()
# #     outcome = yield
# #     rep = outcome.get_result()
# #     setattr(item, "rep_" + rep.when, rep)
# #     return rep
#
#
#
# import pytest
# from selenium import webdriver
#
# @pytest.fixture(scope="session")
# def setup(request):
#     driver = webdriver.Chrome()
#     driver.get("http://www.python.org")
#
#     yield driver
#     driver.close()
#     driver.quit()
#
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(__multicall__):
#     report = __multicall__.execute()
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == 'call':
#         xfail = hasattr(report, 'wasxfail')
#         if (report.skipped and xfail) or (report.failed and not xfail):
#
#             try:
#                 breakpoint()
#                 # attach(data=driver.get_screenshot_as_png(), name='screenshot1')
#             except Exception as e:
#                 print("Error saving screenshot !!")
#
#     return report