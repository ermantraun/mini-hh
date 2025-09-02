import pytest
from fastapi.testclient import TestClient
from api.main import app 
from api.ioc import build_container  



@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_register_success(client):
    payload = {"email": "user@example.com", "password": "secret"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201
    assert resp.json()["email"] == payload["email"]


def test_register_fail(client):
    payload = {"email": "bademail", "password": "short"}
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 400


def test_login_success(client):
    payload = {"email": "user@example.com", "password": "secret"}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_fail(client):
    payload = {"email": "user@example.com", "password": "wrong"}
    resp = client.post("/auth/login", json=payload)
    assert resp.status_code == 401


def test_create_resume(client):
    payload = {"title": "My CV", "content": "Some text"}
    resp = client.post("/resumes", json=payload)
    assert resp.status_code == 201
    assert resp.json()["title"] == payload["title"]


def test_list_resumes(client):
    resp = client.get("/resumes")
    assert resp.status_code == 200
    assert "items" in resp.json()


def test_get_resume(client):
    resp = client.get("/resumes/1")
    if resp.status_code == 200:
        assert resp.json()["id"] == 1
    else:
        assert resp.status_code == 404


def test_update_resume(client):
    payload = {"title": "Updated", "content": "Updated text"}
    resp = client.put("/resumes/1", json=payload)
    if resp.status_code == 200:
        assert resp.json()["title"] == "Updated"
    else:
        assert resp.status_code == 404


def test_delete_resume(client):
    resp = client.delete("/resumes/1")
    assert resp.status_code in (204, 404)


def test_list_improvements(client):
    resp = client.get("/resumes/1/improvements")
    assert resp.status_code in (200, 404)


def test_improve_resume(client):
    resp = client.post("/resumes/1/improvements/improve")
    assert resp.status_code in (200, 404)
