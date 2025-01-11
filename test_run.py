from pages import LoginPage, InventoryPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_auth_invalid_password(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login("standard_user")
    auth_page.input_password("invalid_password")
    auth_page.login_button_click()

    assert driver.current_url == "https://www.saucedemo.com/", "Переход со страницы произошел"
    assert auth_page.is_error_message_displayed("Epic sadface: Username and password do not match any user in this service"), "Сообщение об ошибке не отображается или не соответствует ожидаемому"

def test_auth_empty_password(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login("standard_user")
    auth_page.input_password("")
    auth_page.login_button_click()

    assert driver.current_url == "https://www.saucedemo.com/", "Переход со страницы произошел"
    assert auth_page.is_error_message_displayed("Epic sadface: Password is required"), "Сообщение об ошибке не отображается или не соответствует ожидаемому"

def test_auth_valid_users(driver, login):
    auth_page = LoginPage(driver)
    auth_page.input_login(login)
    auth_page.input_password("secret_sauce")
    auth_page.login_button_click()

    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert driver.current_url == "https://www.saucedemo.com/inventory.html", "URL не соответствует ожидаемому"

    inventory_page = InventoryPage(driver)
    assert inventory_page.check_inventory_page_open(), "Страница инвентаря не открылась"
