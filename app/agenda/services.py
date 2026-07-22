import logging

import requests
from flask import current_app

logger = logging.getLogger(__name__)

CAMPOS_OBRIGATORIOS = [
    "paciente",
    "cpf",
    "medico",
    "especialidade",
    "data",
    "horario",
    "convenio",
    "status",
]


def get_agendamentos():
    """
    Busca os agendamentos na API externa (mockada).
    Retorna sempre um dict no formato:
        {"dados": [...], "erro": None}
        {"dados": [], "erro": "mensagem amigável"}
    Nunca deixa uma exceção subir crua para as rotas.
    """
    url = current_app.config["AGENDA_API_URL"]
    timeout = current_app.config["AGENDA_API_TIMEOUT"]

    try:
        response = requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError:
        logger.error("Falha de conexão ao buscar agendamentos em %s", url)
        return {"dados": [], "erro": "Não foi possível conectar ao serviço de agendamentos."}
    except requests.exceptions.Timeout:
        logger.error("Timeout ao buscar agendamentos em %s", url)
        return {"dados": [], "erro": "O serviço de agendamentos demorou demais para responder."}
    except requests.exceptions.RequestException as exc:
        logger.error("Erro inesperado ao buscar agendamentos: %s", exc)
        return {"dados": [], "erro": "Erro inesperado ao buscar os agendamentos."}

    if response.status_code >= 500:
        logger.error(
            "Serviço de agendamentos indisponível. Status: %s", response.status_code
        )
        return {"dados": [], "erro": "Serviço de agendamentos temporariamente indisponível."}

    if response.status_code != 200:
        logger.error(
            "Resposta inesperada do serviço de agendamentos. Status: %s", response.status_code
        )
        return {"dados": [], "erro": "Não foi possível obter os agendamentos no momento."}

    try:
        dados = response.json()
    except ValueError:
        logger.error("Resposta da API de agendamentos não é um JSON válido.")
        return {"dados": [], "erro": "Resposta inválida do serviço de agendamentos."}

    if not isinstance(dados, list):
        logger.error("Resposta da API de agendamentos não é uma lista.")
        return {"dados": [], "erro": "Formato de resposta inesperado do serviço de agendamentos."}

    if not dados:
        return {"dados": [], "erro": None}

    agendamentos_validos = []
    for item in dados:
        campos_faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in item]
        if campos_faltando:
            logger.warning(
                "Agendamento descartado por campos ausentes %s: %s", campos_faltando, item
            )
            continue
        agendamentos_validos.append(item)

    return {"dados": agendamentos_validos, "erro": None}


def filtrar_agendamentos(agendamentos, termo_busca):
    """Filtra por paciente, CPF ou médico. Entradas vazias/inválidas retornam a lista completa."""
    if not termo_busca or not termo_busca.strip():
        return agendamentos

    termo = termo_busca.strip().lower()
    return [
        item
        for item in agendamentos
        if termo in item.get("paciente", "").lower()
        or termo in item.get("cpf", "").lower()
        or termo in item.get("medico", "").lower()
    ]