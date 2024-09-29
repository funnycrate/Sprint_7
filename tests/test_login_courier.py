import pytest
import requests
import allure
from data import *


@pytest.mark.usefixtures("courier_data")
@allure.suite("Тесты логина курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверка, что курьер может авторизоваться с корректными данными")
    def test_courier_can_login(self, courier_data):
        login, password, first_name = courier_data

        with allure.step(f"Попытка авторизации с логином: {login}, паролем: {password}, именем: {first_name}"):
            response = requests.post(LOGIN_URL, json={"login": login, "password": password})

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200, f"Ожидаемый статус 200, но получен {response.status_code}"
            assert "id" in response.json(), f"Ожидалось, что в ответе будет 'id', но его нет"

    @allure.title("Авторизация без логина")
    @allure.description("Проверка, что запрос без логина возвращает ошибку")
    def test_login_missing_login(self, courier_data):
        _, password, first_name = courier_data

        with allure.step(f"Попытка авторизации без логина, но с паролем: {password} и именем: {first_name}"):
            response = requests.post(LOGIN_URL, json={"password": password})

        with allure.step("Проверка ошибки при авторизации без логина"):
            assert response.status_code == 400, f"Ожидаемый статус 400, но получен {response.status_code}"
            assert response.json().get("message") == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получено {response.json().get('message')}"

    @allure.title("Авторизация без пароля (!!!БАГ!!!)")
    @allure.description("Проверка, что запрос без пароля возвращает ошибку")
    @pytest.mark.xfail()
    def test_login_missing_password(self, courier_data):
        login, _, first_name = courier_data

        with allure.step(f"Попытка авторизации без пароля, но с логином: {login} и именем: {first_name}"):
            response = requests.post(LOGIN_URL, json={"login": login})

        with allure.step("Проверка ошибки при авторизации без пароля"):
            assert response.status_code == 400, f"Ожидаемый статус 400, но получен {response.status_code}"
            assert response.json().get("message") == "Недостаточно данных для входа", \
                f"Ожидалось сообщение 'Недостаточно данных для входа', но получено {response.json().get('message')}"

    @allure.title("Авторизация с неверным логином")
    @allure.description("Проверка, что система возвращает ошибку при неверном логине")
    def test_login_with_invalid_login(self, courier_data):
        _, password, first_name = courier_data
        invalid_login = "invalid_login"

        with allure.step(
                f"Попытка авторизации с неверным логином: {invalid_login}, паролем: {password}, именем: {first_name}"):
            response = requests.post(LOGIN_URL, json={"login": invalid_login, "password": password})

        with allure.step("Проверка ошибки при неверном логине"):
            assert response.status_code == 404, f"Ожидаемый статус 404, но получен {response.status_code}"
            assert response.json().get("message") == "Учетная запись не найдена", \
                f"Ожидалось сообщение 'Учетная запись не найдена', но получено {response.json().get('message')}"

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверка, что система возвращает ошибку при неверном пароле")
    def test_login_with_invalid_password(self, courier_data):
        login, _, first_name = courier_data

        with allure.step(f"Попытка авторизации с логином: {login}, неверным паролем и именем: {first_name}"):
            response = requests.post(LOGIN_URL, json={"login": login, "password": "wrong_password"})

        with allure.step("Проверка ошибки при неверном пароле"):
            assert response.status_code == 404, f"Ожидаемый статус 404, но получен {response.status_code}"
            assert response.json().get("message") == "Учетная запись не найдена", \
                f"Ожидалось сообщение 'Учетная запись не найдена', но получено {response.json().get('message')}"

