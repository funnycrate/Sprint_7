import pytest
from data import register_new_courier_and_return_login_password

@pytest.fixture(scope="session")
def courier_data():
    """Фикстура для создания курьера на всю сессию тестов"""
    courier = register_new_courier_and_return_login_password()
    assert len(courier) == 3, "Курьер не был создан. Полученные данные пустые."
    return courier
