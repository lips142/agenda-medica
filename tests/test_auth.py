import pytest

from app import create_app
from app.config import Config
from app.extensions import db
from app.models import User


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        usuario = User(username="teste", email="teste@teste.com")
        usuario.set_password("senha123")
        db.session.add(usuario)
        db.session.commit()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_valido(client):
    response = client.post(
        "/login",
        data={"identificador": "teste", "senha": "senha123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Sair" in response.get_data(as_text=True)


def test_login_invalido(client):
    response = client.post(
        "/login",
        data={"identificador": "teste", "senha": "senha_errada"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "inválidos" in response.get_data(as_text=True)