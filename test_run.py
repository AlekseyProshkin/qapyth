
from pages import LoginPage, InventoryPage
from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

BASE_URL = "https://www.saucedemo.com"
ERROR_COLOR = "rgba(226, 35, 26, 1)"

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_auth_case_1(driver):
    """Тест на успешную авторизацию с валидными данными."""
    driver.get(BASE_URL)
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('secret_sauce')
    auth_page.login_button_click()
    assert InventoryPage(driver).check_inventory_page_open()

def test_invalid_password_case(driver):
    """Тест на авторизацию с неверным паролем."""
    driver.get(BASE_URL)
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('wrong_password')
    auth_page.login_button_click()
    assert driver.current_url == BASE_URL
    login_error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    expected_error = "Epic sadface: Username and password do not match any user in this service"
    assert login_error_message.text == expected_error
    assert login_error_message.is_displayed()

@pytest.mark.parametrize("username", ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user"])
def test_user_auth_cases(driver, username):
    """Тест на авторизацию с различными пользователями."""
    driver.get(BASE_URL)
    auth_page = LoginPage(driver)
    auth_page.input_login(username)
    auth_page.input_password('secret_sauce')
    auth_page.login_button_click()
    if username == "locked_out_user":
        assert driver.current_url == BASE_URL
        login_error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert expected_error in login_error_message.text
    else:
        expected_url = f"{BASE_URL}/inventory.html"
        assert driver.current_url == expected_url
