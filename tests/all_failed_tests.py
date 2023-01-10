# в файле собраны все тесты, которые должны упасть

import pytest
import time
from data import *
from conftest import open_site
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# C-005. При успешной авторизации происходит перенаправление на страницу, содержащую в URL "redirect_uri"
def test_redirect_to_redirect_uri_after_login(open_site):
    # авторизуемся, проверяем, что в url страницы после редиректа содержится redirect_uri
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").send_keys(valid_password)
    pytest.driver.find_element(By.XPATH, "(//button[@id='kc-login'])").click()
    url = pytest.driver.current_url
    assert "redirect_uri" in url

# C-010. Названия полей и кнопок формы регистрации соответвтуют требованиям
# (поля "Имя", "Фамилия", "Регион", "E-mail или мобильный телефон", "Пароль", "Подтверждание пароля", кнопка "Продолжить")
def test_all_names_of_registration_form_are_ok(open_site):
    pytest.driver.find_element(By.ID, "kc-register").click()
    mainpath = '/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[1]/div[1]/div[1]/span[2]').text == 'Имя'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[1]/div[2]/div[1]/span[2]').text == 'Фамилия'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[2]/div[1]/div[1]/span[2]').text == 'Регион'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[3]/div[1]/span[2]').text == 'E-mail или мобильный телефон'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[4]/div[1]/div[1]/span[2]').text == 'Пароль'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/div[4]/div[2]/div[1]/span[2]').text == 'Подтверждение пароля'
    assert pytest.driver.find_element(By.XPATH, mainpath + '/button[1]').text == 'Продолжить'

# C-017. Поле "email" формы регистрации не принимает невалидные значения:
# - превышение длины локальной части (максимальная допустимая 64 символа)
# - превышение длины доменного имени (максимальная допустимая 63 символа, не включая точку)
# - содержит два дефиса подряд
# - локальная часть начинается и/или заканчивается с - (дефиса)
# - доменная часть начинается и/или заканчивается с - (дефиса)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные валидны, то этот xpath не находится. Ловим ошибку NoSuchElementException и ожидаем, что при валидно заполненных полях эта ошибка и возникнет (то есть что текст-предупреждение НЕ высвечивается)
@pytest.mark.parametrize("negative_input", ['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbb@mail.ru', 'mellotune@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbb.tu', 'mello--tune@mail.ru', '-mellotune-@mail.ru', 'mellotune@-mail-.ru'], ids=['превышение длины лок. части', 'превышение длины дом. части', 'содержит два дефиса подряд', 'лок. часть начинается и/или заканчивается с дефиса', 'дом. часть начинается и/или заканчивается с дефиса'])
def test_email_doesnt_accept_invalid_data_2(negative_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.ID, "address").send_keys(negative_input)
    pytest.driver.find_element(By.ID, "password").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[3]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False

# C-020. Электронный адрес на странице получения кода после регистрации замаскирован звёздочками
def test_email_after_registration_is_hidden(open_site):
    pytest.driver.find_element(By.ID, "kc-register").click()
    # заполняем форму регистрации валидными данными
    pytest.driver.find_element(By.NAME, "firstName").send_keys(russian_chars(7))
    pytest.driver.find_element(By.NAME, "lastName").send_keys(russian_chars(14))
    pytest.driver.find_element(By.ID, "address").send_keys(registration_email)
    a = password_random(10)
    pytest.driver.find_element(By.ID, "password").send_keys(a)
    pytest.driver.find_element(By.ID, "password-confirm").send_keys(a)
    pytest.driver.find_element(By.NAME, 'register').click() # отправляем форму регистрации
    # открывается форма для ввода кода из почты, почта должна быть замаскирована звёздочками
    assert '*' in pytest.driver.find_element(By.XPATH, '(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/p[1])').text

# C-021. Телефонный номер на странице получения кода после регистрации замаскирован звёздочками
def test_email_after_registration_is_hidden(open_site):
    pytest.driver.find_element(By.ID, "kc-register").click()
    # заполняем форму регистрации валидными данными
    pytest.driver.find_element(By.NAME, "firstName").send_keys(russian_chars(7))
    pytest.driver.find_element(By.NAME, "lastName").send_keys(russian_chars(14))
    pytest.driver.find_element(By.ID, "address").send_keys(registration_phone)
    a = password_random(10)
    pytest.driver.find_element(By.ID, "password").send_keys(a)
    pytest.driver.find_element(By.ID, "password-confirm").send_keys(a)
    pytest.driver.find_element(By.NAME, 'register').click() # отправляем форму регистрации
    # открывается форма для ввода кода из почты, почта должна быть замаскирована звёздочками
    assert '*' in pytest.driver.find_element(By.XPATH, '(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/p[1])').text
