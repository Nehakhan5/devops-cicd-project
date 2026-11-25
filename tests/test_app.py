
from app import app, VERSION, WELCOME_MESSAGE


def test_home_page():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_welcome_message():
    with app.test_client() as client:
        response = client.get("/")
        assert WELCOME_MESSAGE.encode() in response.data


def test_application_version():
    with app.test_client() as client:
        response = client.get("/api/version")
        assert response.status_code == 200
        assert response.get_json()["version"] == VERSION


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "healthy"


def test_invalid_route():
    with app.test_client() as client:
        response = client.get("/invalid-page")
        assert response.status_code == 404
