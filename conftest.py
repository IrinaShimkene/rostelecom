import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def open_site():
    pytest.driver = webdriver.Chrome('..\\chromedriver.exe')
    pytest.driver.set_window_size(1024, 600)
    pytest.driver.maximize_window()
    pytest.driver.get('https://b2c.passport.rt.ru')
    pytest.driver.implicitly_wait(10)

    yield

    pytest.driver.quit()






