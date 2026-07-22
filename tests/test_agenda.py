from unittest.mock import patch

import pytest
import requests

from app.agenda.services import get_agendamentos, filtrar_agendamentos
from app import create_app
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


def test_sem_agendamentos_retorna_lista_vazia(app):
    with app.app_context():
        with patch("app.agenda.services.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = []
            resultado = get_agendamentos()

    assert resultado["erro"] is None
    assert resultado["dados"] == []


def test_api_indisponivel_retorna_erro_amigavel(app):
    with app.app_context():
        with patch("app.agenda.services.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError()
            resultado = get_agendamentos()

    assert resultado["dados"] == []
    assert "conectar" in resultado["erro"].lower()


def test_filtrar_por_paciente_inexistente():
    agendamentos = [
        {"paciente": "Maria Souza", "cpf": "111", "medico": "Dr. João"}
    ]
    resultado = filtrar_agendamentos(agendamentos, "Paciente Que Não Existe")
    assert resultado == []


def test_filtrar_com_termo_vazio_retorna_tudo():
    agendamentos = [
        {"paciente": "Maria Souza", "cpf": "111", "medico": "Dr. João"}
    ]
    resultado = filtrar_agendamentos(agendamentos, "")
    assert resultado == agendamentos