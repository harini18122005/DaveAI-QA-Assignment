import requests

from config.settings import API_BASE_URL


REQUEST_TIMEOUT = 10


def test_api_01_get_user_list_page_two():
    response = requests.get(
        f"{API_BASE_URL}/api/users",
        params={"page": 2},
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "data" in body
    assert isinstance(body["data"], list)
    assert body["data"]
    assert body["page"] == 2
    assert body["per_page"] > 0
    assert body["total"] >= len(body["data"])
    assert body["total_pages"] >= 2


def test_api_02_get_single_user_two():
    response = requests.get(
        f"{API_BASE_URL}/api/users/2",
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body

    user = body["data"]
    assert user["id"] == 2
    assert user["first_name"] == "Janet"
    assert user["email"] == "janet.weaver@reqres.in"


def test_api_03_get_nonexistent_user():
    response = requests.get(
        f"{API_BASE_URL}/api/users/23",
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 404
    body = response.json()
    assert body == {}


def test_api_04_login_without_password():
    response = requests.post(
        f"{API_BASE_URL}/api/login",
        json={"email": "peter@klaven"},
        timeout=REQUEST_TIMEOUT,
    )

    assert response.status_code == 400
    body = response.json()
    assert "error" in body
    assert "password" in body["error"].lower()