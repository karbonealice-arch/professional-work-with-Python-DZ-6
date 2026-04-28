import pytest


def check_age(age: int):
    if age >= 18:
        result = 'Доступ разрешён'
    else:
        result = 'Доступ запрещён'
    return result

def check_auth(login: str, password: str):
    if (login == 'admin') and (password == 'password'):
        result = 'Добро пожаловать'
    else:
        result = 'Доступ ограничен'
    return result

def get_cost(weight: int):
    if weight <= 10:
        result = 'Стоимость доставки: 200 руб.'
    else:
        result = 'Стоимость доставки: 500 руб.'
    return result

# тест для задания 1
@pytest.mark.parametrize("age, expected", [
    (17, 'Доступ запрещён'),
    (18, 'Доступ разрешён'),
    (25, 'Доступ разрешён'),
    (0, 'Доступ запрещён'),
    (100, 'Доступ разрешён'),
])
def test_check_age(age, expected):
    assert check_age(age) == expected

# тест для задания 2
@pytest.mark.parametrize("login, password, expected", [
    ('admin', 'password', 'Добро пожаловать'),
    ('admin', 'wrong', 'Доступ ограничен'),
    ('user', 'password', 'Доступ ограничен'),
    ('', '', 'Доступ ограничен'),
    ('admin', 'password123', 'Доступ ограничен'),
])
def test_check_auth(login, password, expected):
    assert check_auth(login, password) == expected

# тест для задания 3
@pytest.mark.parametrize("weight, expected_message", [
    (5, '200'),
    (10, '200'),
    (11, '500'),
    (0, '200'),
    (100, '500'),
])
def test_get_cost(weight, expected_message):
    result = get_cost(weight)
    assert expected_message in result, f"При весе {weight} ожидалось сообщение '{expected_message}', получено '{result}'"