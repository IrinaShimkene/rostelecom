import pytest
import random

valid_email = 'mellotune@mail.ru' # почта зарегистрированного аккаунта
valid_phone = '+79167768460' # телефон зарегистрированного аккаунта
valid_password = '123456789Test' # пароль зарегистрированного аккаунта
registration_email = 'rinoomo@mail.ru' # незарегистрированная почта
registration_phone = '+375299159585' # незарегистрированный телефон

def russian_chars(num):
    text = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def english_chars(num):
    text = 'abcdefghijklmnopqrstuvwxyz'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def number_chars(num):
    text = '0123456789'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def chinese_chars(num):
    text = '的一是不了人我在有他这为之大来以个中上们'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def special_chars(num):
    text = '|/!@#$%^&*()-_=+`~?"№;:[]{}'
    rand_string = ''.join(random.choice(text) for i in range(num))
    return rand_string

def password_random(num): # т.к. в пароле обязаны быть строчнаяб заглавная и спецсимвол/число, прибавляем их в начало. Остаток символов выбирается рандомно
    text = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    text1 = 'abcdefghijklmnopqrstuvwxyz'
    text2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text3 = '+-/*!&$#?=@<>1234567890'
    rand_string =  ''.join(random.choice(text1) for i in range(1)) + ''.join(random.choice(text2) for i in range(1)) + ''.join(random.choice(text3) for i in range(1)) + ''.join(random.choice(text) for i in range(num-3))
    return rand_string

