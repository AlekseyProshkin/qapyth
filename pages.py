from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def input_login(self, username):
        login_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        login_field.clear()
        login_field.send_keys(username)

    def input_password(self, password):
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)

    def login_button_click(self):
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()

    def is_error_message_displayed(self, expected_message):
        error_message = self.driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        return error_message.is_displayed() and expected_message in error_message.text

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    def check_inventory_page_open(self):
        try:
            title = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".title"))
            )
            return title.text.strip().lower() == "products"
        except Exception as e:
            print(f"Ошибка при проверке страницы инвентаря: {e}")
            return False
