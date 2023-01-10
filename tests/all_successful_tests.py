# в файле собраны все тесты, которые должны пройти

import pytest
import time
import random
from data import *
from conftest import open_site
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# C-001. При открытии тестового стенда по умолчанию выбрана форма авторизации по телефону
def test_tab_is_on_phone():
    phone_tab = pytest.driver.find_element(By.ID, 't-btn-tab-phone').get_attribute('class') # находим элемент и получаем значение его атрибута класса
    assert phone_tab == 'rt-tab rt-tab--small rt-tab--active' # если таб на кнопке "телефон", то значение класса будет таким

# C-002. При вводе номера/почты в несоответствующие поля аутентификации таб выбора аутентификации автоматически меняется
def test_tab_changes_according_to_data():
    # кликаем на таб "почта", вставляем телефон в поле логина и кликаем по другому полю для провокации изменений
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_phone)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").click()
    # ожидаем, что таб сменился на поле "телефон"
    phone_tab = pytest.driver.find_element(By.ID, 't-btn-tab-phone').get_attribute('class')
    assert phone_tab == 'rt-tab rt-tab--small rt-tab--active'
    # удаляем текст из поля логина вот так, потому что там поле с маской и clear() не работает
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(Keys.CONTROL + "a")
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(Keys.DELETE)
    # вставляем почту в поле логина и кликаем по другому полю для провокации изменений
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").click()
    # ожидаем, что таб сменился на поле "почта"
    mail_tab = pytest.driver.find_element(By.ID, 't-btn-tab-mail').get_attribute('class')
    assert mail_tab == 'rt-tab rt-tab--small rt-tab--active'

# C-003. Авторизация с валидными телефоном и паролем
def test_valid_phone_and_password_auth():
    # вводим телефон и пароль, кликаем по кнопке "войти", проверяем, что на загруженной странице в заголовке есть надпись "Учётные данные"
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_phone)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").send_keys(valid_password)
    pytest.driver.find_element(By.XPATH, "(//button[@id='kc-login'])").click()
    assert pytest.driver.find_element(By.XPATH, "(//h3[text()='Учетные данные'])")

# C-004. Авторизация с валидными почтой и паролем
def test_valid_mail_and_password_auth():
    # вводим почту и пароль, кликаем по кнопке "войти", проверяем, что на загруженной странице в заголовке есть надпись "Учётные данные"
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").send_keys(valid_password)
    pytest.driver.find_element(By.XPATH, "(//button[@id='kc-login'])").click()
    assert pytest.driver.find_element(By.XPATH, "(//h3[text()='Учетные данные'])")

# C-006. При пустом поле пароля авторизация по почте и номеру телефона не осуществляется
def test_with_mail_but_no_password_auth():
    # ждем, когда подгрузится страница с формой авторизации. Сохраняем url до и после того, как пытаемся авторизоваться с посчтой без пароля
    # Ожидаем, что редиректа в ЛК не будет, а значит адреса этих страниц совпадут
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@id='username'])")))
    url_before_try = pytest.driver.current_url
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").send_keys('')
    pytest.driver.find_element(By.XPATH, "(//button[@id='kc-login'])").click()
    url_after_try = pytest.driver.current_url
    assert url_before_try == url_after_try

# C-007. При пустом поле пароля авторизация по почте и номеру телефона не осуществляется
def test_with_mail_but_no_password_auth():
    # ждем, когда подгрузится страница с формой авторизации. Сохраняем url до и после того, как пытаемся авторизоваться с посчтой без пароля
    # Ожидаем, что редиректа в ЛК не будет, а значит адреса этих страниц совпадут
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//input[@id='username'])")))
    url_before_try = pytest.driver.current_url
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_phone)
    pytest.driver.find_element(By.XPATH, "(//input[@id='password'])").send_keys('')
    pytest.driver.find_element(By.XPATH, "(//button[@id='kc-login'])").click()
    url_after_try = pytest.driver.current_url
    assert url_before_try == url_after_try

# C-008. Через форму восстановления пароля нельзя направить код подтверждения на почту, если не введены в поле "Символы" символы с капчи
def test_no_capcha_no_code_to_email():
    # проверяем, что после попытки отправить код без ввода капчи картинка с капчей остается на странице. Значит, мы не перешли к форме ввода кода
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'reset').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'rt-captcha__image')

# C-009. Через форму восстановления пароля нельзя направить код подтверждения на номер телефона, если не введены в поле "Символы" символы с капчи
def test_no_capcha_no_code_to_email():
    # проверяем, что после попытки отправить код без ввода капчи картинка с капчей остается на странице. Значит, мы не перешли к форме ввода кода
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    pytest.driver.find_element(By.XPATH, "(//input[@id='username'])").send_keys(valid_phone)
    pytest.driver.find_element(By.ID, 'reset').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'rt-captcha__image')

# C-011. Поле "Имя" формы регистрации принимает валидные значения, указанные в требованиях (2-30 символов, только кириллица, допускается тире)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные валидны, то этот xpath не находится. Ловим ошибку NoSuchElementException и ожидаем, что при валидно заполненных полях эта ошибка и возникнет (то есть что текст-предупреждение НЕ высвечивается)
@pytest.mark.parametrize("positive_input", [russian_chars(2), russian_chars(3), russian_chars(29), russian_chars(30), 'Анна-мария'], ids=['2 символа кир.', '3 символа кир.', '29 символов кир.', '30 символов кир.', 'Имя с тире'])
def test_registration_name_accepts_valid_data(positive_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.NAME, "firstName").send_keys(positive_input)
    pytest.driver.find_element(By.NAME, "lastName").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == True

# C-012. Поле "Имя" формы регистрации не принимает невалидные значения (меньше 2 символов кириллицей, больше 30 символов кириллицей, латиница, цифры, иероглифы, спец.символы, пустое значение)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные невалидны, то этот xpath находится. Ожидаем, что при невалидно заполненных полях ошибка NoSuchElementException не возникнет (то есть что текст-предупреждение высвечивается)
@pytest.mark.parametrize("negative_input", [russian_chars(1), russian_chars(31), russian_chars(256), english_chars(15), number_chars(18), chinese_chars(10), special_chars(19)], ids=['1 символ кир.', '31 символ кир.', '256 символов кир.', '15 символов лат.', '18 цифр', '10 иероглифов', '19 спецсимволов'])
def test_registration_name_doesnt_accept_invalid_data(negative_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.NAME, "firstName").send_keys(negative_input)
    pytest.driver.find_element(By.NAME, "lastName").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False

# C-013. Поле "Фамилия" формы регистрации принимает валидные значения, указанные в требованиях (2-30 символов, только кириллица, допускается тире)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные валидны, то этот xpath не находится. Ловим ошибку NoSuchElementException и ожидаем, что при валидно заполненных полях эта ошибка и возникнет (то есть что текст-предупреждение НЕ высвечивается)
@pytest.mark.parametrize("positive_input", [russian_chars(2), russian_chars(3), russian_chars(29), russian_chars(30), 'Бузова-Олечка'], ids=['2 символа кир.', '3 символа кир.', '29 символов кир.', '30 символов кир.', 'Фамилия с тире'])
def test_registration_surname_accepts_valid_data(positive_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.NAME, "lastName").send_keys(positive_input)
    pytest.driver.find_element(By.NAME, "firstName").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[1]/div[2]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == True

# C-014. Поле "Фамилия" формы регистрации не принимает невалидные значения (меньше 2 символов кириллицей, больше 30 символов кириллицей, латиница, цифры, иероглифы, спец.символы, пустое значение)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные невалидны, то этот xpath находится. Ожидаем, что при невалидно заполненных полях ошибка NoSuchElementException не возникнет (то есть что текст-предупреждение высвечивается)
@pytest.mark.parametrize("negative_input", [russian_chars(1), russian_chars(31), russian_chars(256), english_chars(15), number_chars(18), chinese_chars(10), special_chars(19)], ids=['1 символ кир.', '31 символ кир.', '256 символов кир.', '15 символов лат.', '18 цифр', '10 иероглифов', '19 спецсимволов'])
def test_registration_surname_doesnt_accept_invalid_data(negative_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.NAME, "lastName").send_keys(negative_input)
    pytest.driver.find_element(By.NAME, "firstName").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[1]/div[2]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False

# C-015. Поле "email" формы регистрации принимает валидные значения:
# - валидный email, содержащий строчные и заглавные буквы
# - начинающийся с цифры в локальной части email
# - начинающийся с цифры в доменной части email
# - Email c несколькими точками в локальной и доменной части (точки не подряд)
# - Email с дефисом в локальной части email
# - Email с дефисом в доменной части email
# - Email с нижним подчёркиванием в локальной части email
# - Длинный email (локальная часть 64 символа, доменная часть 63 символа без точки)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные валидны, то этот xpath не находится. Ловим ошибку NoSuchElementException и ожидаем, что при валидно заполненных полях эта ошибка и возникнет (то есть что текст-предупреждение НЕ высвечивается)
@pytest.mark.parametrize("positive_input", ['Mellotune@mail.ru', '4ret@mail.ru', 'mellotune@4pda.ru', 'm.e.l.l.o.t.u.n.e@ma.il.ru', 'me-llo@mail.ru', 'mellotune@ma-il.ru', 'mello_tune@mail.ru', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.ru'], ids=['строчные и заглавные', 'нач. с цифры в локальной части', 'нач. с цифры в доменной части', 'неск. точек не подряд в лок. и дом. части', 'дефис в лок. части', 'дефис в дом. части', 'андерскор в лок. части', 'верхняя граница длин лок. и дом. части'])
def test_email_accepts_valid_data(positive_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.ID, "address").send_keys(positive_input)
    pytest.driver.find_element(By.ID, "password").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[3]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == True

# C-016. Поле "email" формы регистрации не принимает невалидные значения:
# - отсутствие @ в email
# - отсутствие локальной части
# - отсутствие доменной части
# - содержит две точки подряд
# - локальная часть начинается и/или заканчивается с . (точки)
# - доменная часть начинается и/или заканчивается с . (точки)
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные невалидны, то этот xpath находится. Ожидаем, что при невалидно заполненных полях ошибка NoSuchElementException не возникнет (то есть что текст-предупреждение высвечивается)
@pytest.mark.parametrize("negative_input", ['mellotunemail.ru', '@gmail.com', 'mellotune@', 'mello..tune@mail.ru', '.mellotune.@mail.ru', 'mellotune@.mail.ru.'], ids=['отсутствие @ в email', 'отсутствие лок. части', 'отсутствие дом. части', 'содержит две точки подряд', 'лок. часть начинается и/или заканчивается с точки', 'дом. часть начинается и/или заканчивается с точки'])
def test_email_doesnt_accept_invalid_data(negative_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.ID, "address").send_keys(negative_input)
    pytest.driver.find_element(By.ID, "password").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[3]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False

# C-018. Поле "Пароль" формы регистрации принимает валидные значения:
# - 8 символов валидного пароля
# - 9 символов валидного пароля
# - 19 символов валидного пароля
# - 20 символов валидного пароля
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# Если данные валидны, то этот xpath не находится. Ловим ошибку NoSuchElementException и ожидаем, что при валидно заполненных полях эта ошибка и возникнет (то есть что текст-предупреждение НЕ высвечивается)
@pytest.mark.parametrize("positive_input", [password_random(8), password_random(9), password_random(19), password_random(20)], ids=['8 символов', '9 символов', '19 символов', '20 символов'])
def test_password_accepts_valid_data(positive_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.ID, "password").send_keys(positive_input)
    pytest.driver.find_element(By.ID, "address").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == True

# C-019. Поле "Пароль" формы регистрации не принимает невалидные значения:
# - менее 8 символов валидного пароля
# - более 20 символов валидного пароля
# - 256 символов латиницей
# - все заглавные, латиница, в пределах 8-20 символов
# - все строчные, латиница, в пределах 8-20 символов
# - кириллица, в пределах 8-20 символов
# - иероглифы, в пределах 8-20 символов
# - спецсимволы, в пределах 8-20 символов
# Если ввести невалидное значение в поле и кликнуть вне поля, то отображается текст с просьбой ввести правильное значение, находящийся под указанным xpath
# # Если данные невалидны, то этот xpath находится. Ожидаем, что при невалидно заполненных полях ошибка NoSuchElementException не возникнет (то есть что текст-предупреждение высвечивается)
@pytest.mark.parametrize("negative_input", [password_random(7), password_random(21), password_random(40), english_chars(256), english_chars(15).upper(), english_chars(13), russian_chars(18), chinese_chars(11), special_chars(9)], ids=['7 символов', '21 символ', '40 символов', '256 лат.', '15 заглавных лат.', '13 строчных лат.', '18 кир.', '11 иероглифы', '9 спецсимволов'])
def test_password_doesnt_accept_invalid_data(negative_input):
    pytest.driver.find_element(By.ID, "kc-register").click()
    pytest.driver.find_element(By.ID, "password").send_keys(negative_input)
    pytest.driver.find_element(By.ID, "address").click()

    temporary = False
    try:
        pytest.driver.find_element(By.XPATH, "(/html[1]/body[1]/div[1]/main[1]/section[2]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/span[1])")
    except NoSuchElementException:
        temporary = True

    assert temporary == False