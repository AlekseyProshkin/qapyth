from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Ввод логина: {username}")
    def input_login(self, username):
        login_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        login_field.clear()
        login_field.send_keys(username)

    @allure.step("Ввод пароля")
    def input_password(self, password):
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

    @allure.step("Нажатие кнопки входа")
    def login_button_click(self):
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()

    @allure.step("Проверка отображения сообщения об ошибке: {expected_message}")
    def is_error_message_displayed(self, expected_message):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        return error_message.is_displayed() and expected_message in error_message.text

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Проверка открытия страницы инвентаря")
    def check_inventory_page_open(self):
        try:
            title = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
            )
            return title.text.strip().lower() == "products"
        except Exception as e:
            print(f"Ошибка при проверке страницы инвентаря: {e}")
            return False

    def add_to_cart(self, product_name):
        product = self.driver.find_element(By.XPATH, f"//div[@class='inventory_item' and contains(., '{product_name}')]")
        add_to_cart_button = product.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        add_to_cart_button.click()

    def get_cart_counter(self):
        cart_counter = self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge")
        return cart_counter.text

    def go_to_cart(self):
        cart_button = self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link")
        cart_button.click()

class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def get_item_count(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, ".cart_item")
        return len(items)

    def get_item_quantity(self):
        quantity = self.driver.find_element(By.CSS_SELECTOR, ".cart_quantity")
        return quantity.text

    def get_item_name(self):
        name = self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name")
        return name.text

    def get_item_price(self):
        price_element = self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_price")
        price_text = price_element.text
        return float(price_text.replace('$', ''))

    def click_checkout(self):
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    def fill_first_name(self, first_name):
        first_name_field = self.driver.find_element(By.ID, "first-name")
        first_name_field.send_keys(first_name)

    def fill_last_name(self, last_name):
        last_name_field = self.driver.find_element(By.ID, "last-name")
        last_name_field.send_keys(last_name)

    def fill_zip_code(self, zip_code):
        zip_code_field = self.driver.find_element(By.ID, "postal-code")
        zip_code_field.send_keys(zip_code)

    def click_continue(self):
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

    def get_item_count(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, ".cart_item")
        return len(items)

    def get_item_name(self):
        name = self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_name")
        return name.text

    def get_item_price(self):
        price_element = self.driver.find_element(By.CSS_SELECTOR, ".inventory_item_price")
        price_text = price_element.text
        return float(price_text.replace('$', ''))

    def get_payment_info(self):
        try:
            payment_info = self.driver.find_element(By.CSS_SELECTOR, ".summary_value_label[data-test='payment-info-value']")
            return payment_info.text
        except:
            print("Current URL:", self.driver.current_url)
            print("Page source:", self.driver.page_source)
            return "Payment info not found"

    def get_shipping_info(self):
        try:
            shipping_info = self.driver.find_element(By.CSS_SELECTOR, ".summary_value_label[data-test='shipping-info-value']")
            return shipping_info.text
        except:
            print("Current URL:", self.driver.current_url)
            print("Page source:", self.driver.page_source)
            return "Shipping info not found"

    def get_item_total(self):
        total_element = self.driver.find_element(By.CSS_SELECTOR, ".summary_subtotal_label")
        total_text = total_element.text
        return float(total_text.replace("Item total: $", ""))

    def get_tax(self):
        tax_element = self.driver.find_element(By.CSS_SELECTOR, ".summary_tax_label")
        tax_text = tax_element.text
        return tax_text.replace("Tax: $", "")

    def get_total(self):
        total_element = self.driver.find_element(By.CSS_SELECTOR, ".summary_total_label")
        total_text = total_element.text
        return total_text.replace("Total: $", "")

    def click_finish(self):
        finish_button = self.driver.find_element(By.ID, "finish")
        finish_button.click()

class CheckoutCompletePage:
    def __init__(self, driver):
        self.driver = driver

    def get_complete_header(self):
        header_element = self.driver.find_element(By.CSS_SELECTOR, "span.title")
        return header_element.text

    def get_thank_you_text(self):
        thank_you_element = self.driver.find_element(By.CSS_SELECTOR, "h2.complete-header")
        return thank_you_element.text

    def get_dispatch_text(self):
        dispatch_element = self.driver.find_element(By.CSS_SELECTOR, "div.complete-text")
        return dispatch_element.text

    def back_home_button_is_present(self):
        back_home_button = self.driver.find_elements(By.ID, "back-to-products")
        return len(back_home_button) > 0

    def click_back_home(self):
        back_home_button = self.driver.find_element(By.ID, "back-to-products")
        back_home_button.click()
