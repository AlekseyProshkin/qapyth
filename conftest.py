import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
