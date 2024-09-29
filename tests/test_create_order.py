import pytest
import requests
import allure
from data import *


@allure.suite("Тесты создания заказов")
class TestCreateOrder:

    @allure.title("Параметризованный тест создания заказа")
    @allure.description("Проверка создания заказа с различными вариантами цветов: BLACK, GREY, BLACK и GREY, без указания цвета")
    @pytest.mark.parametrize("color", [
        (["BLACK"], "Цвет BLACK"),       # Тест с цветом BLACK
        (["GREY"], "Цвет GREY"),         # Тест с цветом GREY
        (["BLACK", "GREY"], "Оба цвета"),  # Тест с обоими цветами
        ([], "Без указания цвета")        # Тест без указания цвета
    ])
    def test_create_order_with_colors(self, color):
        """Параметризованный тест создания заказа с разными цветами"""
        color_value, color_desc = color

        payload = {
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-09-29",
            "comment": "Saske, come back to Konoha"
        }

        # Добавляем цвет, если он указан
        if color_value:
            payload["color"] = color_value

        with allure.step(f"Отправка запроса на создание заказа ({color_desc})"):
            response = requests.post(ORDER_URL, json=payload)

        with allure.step(f"Проверка успешного создания заказа ({color_desc})"):
            assert response.status_code == 201, f"Ожидаемый статус 201, но получен {response.status_code}"
            assert "track" in response.json(), f"Ожидалось, что в ответе будет 'track', но его нет"
