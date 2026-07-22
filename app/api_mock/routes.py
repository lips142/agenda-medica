from flask import Blueprint, jsonify

from app.api_mock.data import AGENDAMENTOS

api_mock_bp = Blueprint("api_mock", __name__)


@api_mock_bp.route("/agendamentos", methods=["GET"])
def listar_agendamentos():
    return jsonify(AGENDAMENTOS), 200