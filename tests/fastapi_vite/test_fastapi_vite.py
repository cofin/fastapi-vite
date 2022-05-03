# Third Party Libraries
from starlette.testclient import TestClient

# Fastapi Vite
from fastapi_vite import __version__


def test_version():
    assert __version__ == "0.3.2"


def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == "index.html"
    assert "request" in response.context
