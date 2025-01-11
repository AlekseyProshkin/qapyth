import allure
from pages import LoginPage, InventoryPage, CartPage, CheckoutPage, CheckoutCompletePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


@allure.title("Тест на неверный пароль")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("TMS-001")
def test_auth_invalid_password(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login("standard_user")
    auth_page.input_password("invalid_password")
    auth_page.login_button_click()

    assert driver.current_url == "https://www.saucedemo.com/", "Переход со страницы произошел"
    assert auth_page.is_error_message_displayed("Epic sadface: Username and password do not match any user in this service"), "Сообщение об ошибке не отображается или не соответствует ожидаемому"

@allure.title("Тест на пустой пароль")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("TMS-002")
def test_auth_empty_password(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login("standard_user")
    auth_page.input_password("")
    auth_page.login_button_click()

    assert driver.current_url == "https://www.saucedemo.com/", "Переход со страницы произошел"
    assert auth_page.is_error_message_displayed("Epic sadface: Password is required"), "Сообщение об ошибке не отображается или не соответствует ожидаемому"

@allure.title("Тест на валидные логины")
@allure.severity(allure.severity_level.NORMAL)
@allure.testcase("TMS-003")
def test_auth_valid_users(driver, login):
    auth_page = LoginPage(driver)
    auth_page.input_login(login)
    auth_page.input_password("secret_sauce")
    auth_page.login_button_click()

    try:
        WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
        assert driver.current_url == "https://www.saucedemo.com/inventory.html", "URL не соответствует ожидаемому"

        inventory_page = InventoryPage(driver)
        assert inventory_page.check_inventory_page_open(), "Страница инвентаря не открылась"
    except TimeoutException:
        error_message = auth_page.is_error_message_displayed("Epic sadface: Sorry, this user has been locked out.")
        assert error_message, "Ожидаемое сообщение об ошибке не отображается"
        allure.attach("Пользователь заблокирован", name="Ошибка", attachment_type=allure.attachment_type.TEXT)


@allure.title("Тест на пустые поля логина и пароля")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("TMS-004")
@allure.issue("ISSUE-1", "Тест заведомо падает")
def test_empty_login_and_password(driver):
    auth_page = LoginPage(driver)

    with allure.step("Проверка, что поле логина пустое"):
        login_field = driver.find_element(By.ID, "user-name")
        assert login_field.get_attribute("value") == "", "Поле логина не пустое"

    with allure.step("Проверка, что поле пароля пустое"):
        password_field = driver.find_element(By.ID, "password")
        assert password_field.get_attribute("value") == "", "Поле пароля не пустое"

    with allure.step("Нажатие кнопки Login"):
        auth_page.login_button_click()

    with allure.step("Проверка, что переход с текущей страницы не произошел"):
        assert driver.current_url == "https://www.saucedemo.com", "Переход со страницы произошел"

    with allure.step("Проверка сообщения об ошибке"):
        error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        assert error_message.is_displayed(), "Сообщение об ошибке не отображается"
        assert "Epic sadface: Password is required" in error_message.text, "Сообщение об ошибке не соответствует ожидаемому"

@allure.title("Тест на полный цикл покупки")
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase("TMS-005")
def test_full_purchase_cycle(driver):
    # Шаг 1: Авторизация
    with allure.step("Авторизация на странице https://www.saucedemo.com/"):
        login_page = LoginPage(driver)
        login_page.input_login("standard_user")
        login_page.input_password("secret_sauce")
        login_page.login_button_click()

    # Шаг 2-3: Добавление товара в корзину
    with allure.step("Добавление Sauce Labs Backpack в корзину"):
        inventory_page = InventoryPage(driver)
        inventory_page.add_to_cart("Sauce Labs Backpack")
        assert inventory_page.get_cart_counter() == "1", "Количество товаров в корзине не равно 1"

    # Шаг 4: Переход в корзину
    with allure.step("Переход в корзину"):
        inventory_page.go_to_cart()

    # Шаг 5: Проверка содержимого корзины
    with allure.step("Проверка содержимого корзины"):
        cart_page = CartPage(driver)
        assert cart_page.get_item_count() == 1, "Количество товаров в корзине не равно 1"
        assert cart_page.get_item_quantity() == "1", "Количество единиц товара не равно 1"
        assert "Sauce Labs Backpack" in cart_page.get_item_name(), "Название товара не соответствует ожидаемому"
        item_price = cart_page.get_item_price()
        assert item_price > 0, "Цена товара не определена или равна нулю"

    # Шаг 6: Переход к оформлению заказа
    with allure.step("Переход к оформлению заказа"):
        cart_page.click_checkout()

    # Шаг 7-8: Заполнение данных покупателя
    with allure.step("Заполнение данных покупателя"):
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_first_name("Joe")
        checkout_page.fill_last_name("Lowson")
        checkout_page.fill_zip_code("1234")
        checkout_page.click_continue()

    # Шаг 9: Проверка информации о заказе
    with allure.step("Проверка информации о заказе"):
        assert checkout_page.get_item_count() == 1, "Количество товаров в заказе не равно 1"
        assert "Sauce Labs Backpack" in checkout_page.get_item_name(), "Название товара не соответствует ожидаемому"
        assert checkout_page.get_item_price() == item_price, "Цена товара не соответствует цене на странице товаров"
        payment_info = checkout_page.get_payment_info()
        assert "SauceCard #31337" in payment_info, f"Информация о платеже не соответствует ожидаемой. Получено: {payment_info}"
        shipping_info = checkout_page.get_shipping_info()
        assert "Free Pony Express Delivery!" in shipping_info, f"Информация о доставке не соответствует ожидаемой. Получено: {shipping_info}"
        assert checkout_page.get_item_total() == item_price, "Общая стоимость товаров не соответствует цене товара"
        assert checkout_page.get_tax() == "2.40", "Сумма налога не соответствует ожидаемой"
        assert checkout_page.get_total() == str(
            float(item_price) + 2.40), "Общая стоимость заказа не соответствует сумме цены товара и налога"

    # Шаг 10: Завершение заказа
    with allure.step("Завершение заказа"):
        checkout_page.click_finish()

    # Шаг 11: Проверка завершения заказа
    with allure.step("Проверка завершения заказа"):
        complete_page = CheckoutCompletePage(driver)
        assert complete_page.get_complete_header() == "Checkout: Complete!", "Заголовок завершения заказа не соответствует ожидаемому"
        assert complete_page.get_thank_you_text() == "Thank you for your order!", "Текст благодарности не соответствует ожидаемому"
        assert complete_page.get_dispatch_text() == "Your order has been dispatched, and will arrive just as fast as the pony can get there!", "Текст о доставке не соответствует ожидаемому"
        assert complete_page.back_home_button_is_present(), "Кнопка 'Back Home' отсутствует"

    with allure.step("Возврат на главную страницу"):
        complete_page.click_back_home()
        assert driver.current_url == "https://www.saucedemo.com/inventory.html", "Не удалось вернуться на главную страницу"