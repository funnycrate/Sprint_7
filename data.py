import random
import string
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
COURIER_URL = f"{BASE_URL}/courier"
LOGIN_URL = f"{COURIER_URL}/login"
ORDER_URL = f"{BASE_URL}/orders"

# Генерация случайной строки
def generate_random_string(length):
    """Генерирует строку случайных символов заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Метод регистрации нового курьера возвращает список из логина, пароля и имени
def register_new_courier_and_return_login_password():
    """Генерирует данные и регистрирует нового курьера. Возвращает логин, пароль и имя."""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(COURIER_URL, json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []

# Метод для создания уникального логина, добавляя к нему случайные символы
def create_unique_login(base_login, suffix_length=2):
    """Добавляет к базовому логину случайные символы, чтобы сделать его уникальным."""
    random_suffix = generate_random_string(suffix_length)
    return base_login + random_suffix


def get_courier_id(login, password):
    """Авторизует курьера и возвращает его id"""
    response = requests.post(LOGIN_URL, json={"login": login, "password": password})

    if response.status_code == 200:
        return response.json().get("id")  # Извлекаем id курьера
    return None  # Если не удалось авторизоваться, возвращаем None