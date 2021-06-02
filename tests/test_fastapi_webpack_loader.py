from fastapi_vite import __version__
from starlette.testclient import TestClient


def test_version():
    assert __version__ == '0.1.0'


def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "request" in response.context
