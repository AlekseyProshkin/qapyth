from pages import LoginPage, InventoryPage


def test_auth(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('secret_sauce')
    auth_page.login_button_click()

    assert InventoryPage(driver).check_inventory_page_open()
