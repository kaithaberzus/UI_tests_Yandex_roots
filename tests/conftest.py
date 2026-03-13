import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.block_with_started_window import BlockWithStartedWindow
from data import Addresses
from pages.block_with_ordering_a_taxi import BlockWithOrderingATaxi
from pages.block_with_choosing_route import BlockWithChoosingRoute


# Фикстура создания драйвера для хрома
@pytest.fixture
def driver():
    options = Options()
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()

# Фикстура заполнения стартового блока
@pytest.fixture
def fill_started_block(driver):
    bwsw = BlockWithStartedWindow(driver)
    adr = Addresses()

    bwsw.open_main_page()
    bwsw.fill_input_to(adr.ADDRESS_HAM_VAL)
    bwsw.fill_input_from(adr.ADDRESS_ZUB_VAL)

    yield

# Викстура вызова такси в тарифе рабочий со столиком для ноутбука
@pytest.fixture
def get_taxi(driver, fill_started_block):
    bwoat = BlockWithOrderingATaxi(driver)
    bwcar = BlockWithChoosingRoute(driver)

    bwcar.click_to_the_button_call_a_taxi()
    cost = bwoat.get_price_of_tariff_worker().replace(' ₽', '')
    bwoat.scrolling_to_block_req_to_the_order()
    bwoat.click_to_the_block_req_to_the_order()
    bwoat.scrolling_to_checkbox_table_for_laptop()
    bwoat.choose_checkbox_table_for_laptop()
    bwoat.scrolling_to_the_button_order_taxi()
    bwoat.click_to_the_button_order_taxi()

    yield cost