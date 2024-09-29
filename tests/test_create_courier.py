import pytest
import requests
import allure
from data import *

@allure.suite("Тесты создания курьеров")
@pytest.mark.usefixtures('courier_data')
class TestCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверка успешного создания курьера с модифицированным логином")
    def test_create_courier_success(self, courier_data):
        login, password, first_name = courier_data

        with allure.step("Создание уникального логина"):
            unique_login = create_unique_login(login)

        with allure.step("Создание курьера с новым уникальным логином"):
            response = requests.post(COURIER_URL, json={
                "login": unique_login,
                "password": password,
                "firstName": first_name
            })

        with allure.step("Проверка успешного создания курьера"):
            assert response.status_code == 201, f"Ожидаемый статус 201, но получен {response.status_code}"
            assert response.json() == {"ok": True}, f"Ожидался ответ {{'ok': True}}, но получен {response.json()}"

    @allure.title("Создание дубликата курьера")
    @allure.description("Проверка невозможности создания двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier_data):
        login, password, first_name = courier_data

        with allure.step("Попытка создания курьера с тем же логином"):
            response = requests.post(COURIER_URL, json={
                "login": login,
                "password": password,
                "firstName": first_name
            })

        with allure.step("Проверка ошибки при создании дубликата"):
            assert response.status_code == 409, f"Ожидаемый статус 409, но получен {response.status_code}"
            assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой.", \
                f"Ожидалось сообщение 'Этот логин уже используется. Попробуйте другой.', но получено {response.json().get('message')}"

    @allure.title("Создание курьера без логина")
    @allure.description("Проверка ошибки при создании курьера без логина")
    def test_create_courier_missing_login(self, courier_data):
        _, password, first_name = courier_data

        with allure.step(f"Попытка создания курьера без логина, но с паролем: {password} и именем: {first_name}"):
            payload = {
                "password": password,
                "firstName": first_name
            }
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверка ошибки при создании курьера без логина"):
            assert response.status_code == 400, f"Ожидаемый статус 400, но получен {response.status_code}"
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи", \
                f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', но получено {response.json().get('message')}"

    @allure.title("Создание курьера без пароля")
    @allure.description("Проверка ошибки при создании курьера без пароля")
    def test_create_courier_missing_password(self, courier_data):
        login, _, first_name = courier_data

        with allure.step(f"Попытка создания курьера без пароля, но с логином: {login} и именем: {first_name}"):
            payload = {
                "login": login,
                "firstName": first_name
            }
            response = requests.post(COURIER_URL, json=payload)

        with allure.step("Проверка ошибки при создании курьера без пароля"):
            assert response.status_code == 400, f"Ожидаемый статус 400, но получен {response.status_code}"
            assert response.json().get("message") == "Недостаточно данных для создания учетной записи", \
                f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', но получено {response.json().get('message')}"
