import requests
import time

BASE_URL = "http://localhost:8080/api/v1/store"

# --- Existing Happy Path Test (kept for reference) ---
def test_happy_path():
    sample_key_value = {"key": "test_key", "value": "test_value"}
    updated_value = {"value": "updated_value"}

    # Create a new key-value pair
    create_response = requests.post(BASE_URL, json=sample_key_value)
    assert create_response.status_code == 201

    # Retrieve the key-value pair
    get_response = requests.get(f"{BASE_URL}/{sample_key_value['key']}")
    assert get_response.status_code == 200

    # Update the key-value pair
    update_response = requests.put(f"{BASE_URL}/{sample_key_value['key']}", json=updated_value)
    assert update_response.status_code == 200

    # Delete the key-value pair
    delete_response = requests.delete(f"{BASE_URL}/{sample_key_value['key']}")
    assert delete_response.status_code == 200


# --- Additional Tests for Error Scenarios ---
def test_create_missing_key_value():
    invalid_data = {"key": "test_key"}
    response = requests.post(BASE_URL, json=invalid_data)
    assert response.status_code == 400


def test_create_duplicate_key():
    sample_key_value = {"key": "duplicate_key", "value": "first_value"}
    requests.post(BASE_URL, json=sample_key_value)  # First create
    duplicate_response = requests.post(BASE_URL, json=sample_key_value)  # Duplicate create
    assert duplicate_response.status_code == 400


def test_get_non_existent_key():
    response = requests.get(f"{BASE_URL}/non_existent_key")
    assert response.status_code == 404


def test_update_non_existent_key():
    updated_value = {"value": "updated_value"}
    response = requests.put(f"{BASE_URL}/non_existent_key", json=updated_value)
    assert response.status_code == 404


def test_delete_non_existent_key():
    response = requests.delete(f"{BASE_URL}/non_existent_key")
    assert response.status_code == 404
