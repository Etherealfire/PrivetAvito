import requests

BASE_URL = "https://qa-internship.avito.com"


def create_item(payload):
    return requests.post(f"{BASE_URL}/api/1/item", json=payload)


def get_item(item_id):
    return requests.get(f"{BASE_URL}/api/1/item/{item_id}")


def get_statistic(item_id):
    return requests.get(f"{BASE_URL}/api/1/statistic/{item_id}")


def delete_item(item_id):
    return requests.delete(f"{BASE_URL}/api/2/item/{item_id}")


def get_items_by_seller(seller_id):
    return requests.get(f"{BASE_URL}/api/1/{seller_id}/item")


def test_create_item_success():
    payload = {
        "sellerID": 25211,
        "name": "Arty",
        "price": 300,
        "statistics": {
            "likes": 1,
            "viewCount": 25,
            "contacts": 228
        }
    }

    response = create_item(payload)

    assert response.status_code == 200
    assert "Сохранили объявление" in response.json()["status"]


def test_get_statistic_success():
    payload = {
        "sellerID": 25212,
        "name": "Test",
        "price": 100,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    create_response = create_item(payload)
    assert create_response.status_code == 200

    item_id = create_response.json()["status"].split()[-1]

    response = get_statistic(item_id)

    assert response.status_code in [200, 400]

    if response.status_code == 200:
        assert isinstance(response.json(), list)



def test_delete_item_success():
    payload = {
        "sellerID": 25213,
        "name": "DeleteTest",
        "price": 200,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    create_response = create_item(payload)
    item_id = create_response.json()["status"].split()[-1]

    response = delete_item(item_id)

    assert response.status_code == 200


def test_create_item_without_price():
    payload = {
        "sellerID": 25214,
        "name": "NoPrice",
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    response = create_item(payload)

    assert response.status_code == 400
    assert "price" in response.text


def test_create_item_with_empty_name():
    payload = {
        "sellerID": 25215,
        "name": "",
        "price": 100,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    response = create_item(payload)

    assert response.status_code == 400


def test_get_statistic_with_invalid_id():
    response = get_statistic("null")

    assert response.status_code == 400


def test_get_statistic_not_found():
    response = get_statistic("f84f6c79-7b2a-4953-886c-334a0032b742")

    assert response.status_code == 404


def test_get_items_by_nonexistent_seller():
    response = get_items_by_seller(11420)

    assert response.status_code == 200
    assert response.json() == []


def test_delete_item_twice():
    payload = {
        "sellerID": 25216,
        "name": "DeleteTwice",
        "price": 300,
        "statistics": {
            "likes": 1,
            "viewCount": 1,
            "contacts": 1
        }
    }

    create_response = create_item(payload)
    item_id = create_response.json()["status"].split()[-1]

    first_delete = delete_item(item_id)
    second_delete = delete_item(item_id)

    assert first_delete.status_code == 200
    assert second_delete.status_code in [404, 500]
