import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from allure_commons.model2 import Status

@pytest.fixture(autouse=True)
def navigate_to_login_page(driver):
    driver.get("https://www.saucedemo.com")

@pytest.fixture(params=[
    "standard_user",
    "locked_out_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
])
def login(request):
    return request.param

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument('--enable-javascript')
    _driver = webdriver.Chrome(options=options)
    yield _driver
    _driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            web_driver = item.funcargs["driver"]
            try:
                allure.attach(
                    web_driver.get_screenshot_as_png(),
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")

        rep.status = Status.FAILED
