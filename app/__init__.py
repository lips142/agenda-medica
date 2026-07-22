import logging

from flask import Flask
from flask_login import LoginManager

from app.config import Config
from app.extensions import db

logger = logging.getLogger(__name__)
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar a agenda."

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.agenda.routes import agenda_bp
    from app.api_mock.routes import api_mock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(api_mock_bp, url_prefix="/api")

    register_error_handlers(app)
    register_cli_commands(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return "Pagina nao encontrada.", 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.exception("Erro interno não tratado.")
        return "Ocorreu um erro interno. Tente novamente mais tarde.", 500


def register_cli_commands(app):
    @app.cli.command("fetch-agenda")
    def fetch_agenda_command():
        """Busca e imprime os agendamentos no terminal."""
        from app.agenda.services import get_agendamentos

        resultado = get_agendamentos()
        if resultado.get("erro"):
            print(f"Erro ao buscar agendamentos: {resultado['erro']}")
            return
        for item in resultado.get("dados", []):
            print(
                f"{item.get('data')} {item.get('horario')} | "
                f"{item.get('paciente')} ({item.get('cpf')}) | "
                f"{item.get('medico')} - {item.get('especialidade')} | "
                f"{item.get('convenio')} | {item.get('status')}"
            )