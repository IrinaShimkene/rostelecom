# rostelecom
Данные тестовые сценарии проверяют форму регистрации, авторизации и восстановления пароля для частных клиентов компании "Ростелеком": https://b2c.passport.rt.ru/account_b2c/page

Тесты были написаны, основываясь на требованиях, предоставленных заказчиком: https://docs.google.com/document/d/1Sgww3tOzIzVOqYHdMNu0oWd8PQe6nv-F/edit?usp=sharing&ouid=104445533477470531867&rtpof=true&sd=true

**!!! ШАГИ РАБОТЫ НАД ПРОЕКТОМ, ВОПРОСЫ ЗАКАЗЧИКУ ПО ТРЕБОВАНИЯМ, ТЕСТ-КЕЙСЫ, БАГ-РЕПОРТЫ, ИСПОЛЬЗОВАННЫЕ ТЕХНИКИ ТЕСТ-ДИЗАЙНА И НАПИСАНИЯ КОДА ТЕСТОВ ПРЕДСТАВЛЕНЫ В ФАЙЛЕ: https://docs.google.com/document/d/16Mq0_O1tIoWIveOX-iZjrgpS5ezJQN9bG8wXvkyGQuo/edit?usp=sharing**

В папке tests представлены 2 файла: 
- all_successful_tests.py содержит 16 успешных автотестов, как позитивных, так и негативных. То есть тестов, которые подтверждают ожидаемое поведение платформы;
- all_failed_tests.py содержит 5 упавших тестов, с помощью которых были найдены ошибки в работе платформы.

Для запуска тестов необходимо:
- установить библиотеки из файла requirements.txt, набрав в терминале pip install -r requirements.txt
- тесты написаны для Chrome браузера, установите драйвер для вашей версии браузера отсюда: https://chromedriver.chromium.org/downloads
- для запуска тестов перейдите в папку tests через терминал, используя команду cd "здесь без ковычек указан полный путь до папки с тестами"
- тесты запускаются командой из терминала: pytest -s -v --driver Chrome --driver-path "полный путь до драйвера Chrome без кавычек" "название запускаемого файла без кавычек, например, all_successful_tests.py"
