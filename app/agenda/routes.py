from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from app.agenda.services import get_agendamentos, filtrar_agendamentos

agenda_bp = Blueprint("agenda", __name__)


@agenda_bp.route("/")
@login_required
def index():
    return render_template("agenda.html")


@agenda_bp.route("/api/agenda/dados")
@login_required
def dados_agenda():
    resultado = get_agendamentos()

    if resultado["erro"]:
        return jsonify({"erro": resultado["erro"]}), 503

    termo_busca = request.args.get("busca", "")
    agendamentos = filtrar_agendamentos(resultado["dados"], termo_busca)

    return jsonify({"dados": agendamentos, "erro": None}), 200