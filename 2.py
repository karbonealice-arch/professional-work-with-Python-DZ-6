import time
import requests
import pytest
import os


BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
TOKEN = os.getenv("YANDEX_TOKEN")

if not TOKEN:
    pytest.skip("Переменная окружения YANDEX_TOKEN не установлена", allow_module_level=True)

HEADERS = {"Authorization": f"OAuth {TOKEN}"}


def create_folder(path: str):
    params = {"path": path}
    return requests.put(BASE_URL, headers=HEADERS, params=params)


def delete_folder(path: str):
    params = {"path": path, "permanently": True}
    return requests.delete(BASE_URL, headers=HEADERS, params=params)


def folder_exists(path: str) -> bool:
    params = {"path": path}
    resp = requests.get(BASE_URL, headers=HEADERS, params=params)
    return resp.status_code == 200


@pytest.fixture
def unique_folder():
    folder_name = f"test_folder_{int(time.time())}"
    yield folder_name
    if folder_exists(folder_name):
        delete_folder(folder_name)


# позитивные тесты
def test_create_folder_success(unique_folder):
    resp = create_folder(unique_folder)
    assert resp.status_code == 201, f"Ожидался код 201, получен {resp.status_code}"
    assert folder_exists(unique_folder), "Папка не найдена после создания"


# негативные тесты
def test_create_folder_already_exists(unique_folder):
    create_folder(unique_folder)
    resp = create_folder(unique_folder)
    assert resp.status_code == 409, "При повторном создании папки должен был быть код 409"
    error_data = resp.json()
    assert error_data.get("error") == "DiskPathPointsToExistentDirectoryError", "Ошибка при дублировании папки"


def test_create_folder_invalid_token():
    bad_headers = {"Authorization": "OAuth wrong_token"}
    resp = requests.put(BASE_URL, headers=bad_headers, params={"path": "any_folder"})
    assert resp.status_code == 401, "Неверный токен, ожидался код 401"


@pytest.mark.parametrize("bad_path", [
    "folder/with/slash",
    "../../../etc",
    "?invalid*",
    "",
])
def test_create_folder_invalid_name(bad_path):
    resp = create_folder(bad_path)
    assert resp.status_code in (400, 409), f"Для пути {bad_path} ожидался ответ 400/409, получено {resp.status_code}"