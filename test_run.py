# ui_project/tests/test_login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest

# Фикстура для инициализации и закрытия браузера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # При необходимости можете добавить опции
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_case_1(driver):
    # Шаг 1
    driver.get("https://www.saucedemo.com")

    # Шаг 2
    valid_username = "standard_user"
    driver.find_element(By.ID, "user-name").send_keys(valid_username)

    # Шаг 3
    invalid_password = "wrong_password"
    driver.find_element(By.ID, "password").send_keys(invalid_password)

    # Шаг 4
    driver.find_element(By.ID, "login-button").click()

    # Шаг 5a: Проверка, что URL не изменился
    assert driver.current_url == "https://www.saucedemo.com/"

    # Шаг 5b: Проверка сообщения об ошибке
    error_element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    expected_error = "Epic sadface: Username and password do not match any user in this service"
    assert error_element.text == expected_error

    # Дополнительная проверка: сообщение должно быть отображено
    assert error_element.is_displayed()

def test_case_2(driver):

    # Шаг 1
    driver.get("https://www.saucedemo.com")

    # Шаг 2
    valid_username = "standard_user"
    driver.find_element(By.ID, "user-name").send_keys(valid_username)

    # Шаг 3: Оставляем поле пароля пустым

    # Шаг 4
    driver.find_element(By.ID, "login-button").click()

    # Шаг 5a: Проверка, что URL не изменился
    assert driver.current_url == "https://www.saucedemo.com/"

    # Шаг 5b: Проверка сообщения об ошибке
    error_element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    expected_error = "Epic sadface: Password is required"
    assert error_element.text == expected_error

    # Проверка, что сообщение отображается
    assert error_element.is_displayed()

    # Проверка цвета фона родительского элемента
    error_container = driver.find_element(By.CSS_SELECTOR, "div.error-message-container")
    background_color = error_container.value_of_css_property("background-color")
    print("Background color:", background_color)
    assert background_color == "rgba(226, 35, 26, 1)"  # Обновите значение при необходимости


@pytest.mark.parametrize("username", ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"])
def test_case_3(driver, username):
    # Шаг 1
    driver.get("https://www.saucedemo.com")

    # Шаг 2a
    driver.find_element(By.ID, "user-name").send_keys(username)

    # Шаг 2b
    valid_password = "secret_sauce"
    driver.find_element(By.ID, "password").send_keys(valid_password)

    # Шаг 2c
    driver.find_element(By.ID, "login-button").click()

    # Шаг 2d
    if username == "locked_out_user":
        # Проверка для заблокированного пользователя
        assert driver.current_url == "https://www.saucedemo.com/"
        error_element = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        assert expected_error in error_element.text
    else:
        # Проверка для остальных пользователей
        expected_url = "https://www.saucedemo.com/inventory.html"
        assert driver.current_url == expected_url

