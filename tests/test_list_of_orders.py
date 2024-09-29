import pytest
import requests
import allure
from data import *


@allure.suite("Тесты списка заказов")
class TestListOfOrders:

    @allure.title("Получение списка всех заказов для курьера")
    @allure.description("Проверка, что запрос к /orders возвращает список заказов для созданного курьера")
    def test_get_all_orders_for_created_courier(self, courier_data):
        """Проверка получения списка заказов для созданного курьера"""
        # Получаем логин, пароль и имя из фикстуры courier_data
        login, password, first_name = courier_data

        courier_id = get_courier_id(login, password)
        assert courier_id is not None, "Не удалось получить id курьера при авторизации"

        with allure.step(f"Отправка GET-запроса на получение списка заказов для courierId: {courier_id}"):
            response = requests.get(ORDER_URL, params={"courierId": courier_id})

        with allure.step("Проверка успешного получения списка заказов"):
            assert response.status_code == 200, f"Ожидаемый статус 200, но получен {response.status_code}"
            assert "orders" in response.json(), f"Ожидалось, что в ответе будет поле 'orders', но его нет"
            assert isinstance(response.json()["orders"], list), "Ожидалось, что 'orders' будет списком, но получено другое значение"