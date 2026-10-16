#     python -m pytest test_first.py

import sys
import pytest
import requests


def fetch_user_name(user_id):
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    data = resp.json()
    return data["name"]


def test_fetch_user_name(mocker):
    fake_resp = mocker.Mock()
    fake_resp.json.return_value = {"name": "小明", "id": 1}
    mocker.patch("requests.get", return_value = fake_resp)

    name = fetch_user_name(1)
    assert name == "小明"
    requests.get.assert_called_once_with("https://api.example.com/users/1")
