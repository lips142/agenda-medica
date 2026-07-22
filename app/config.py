import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-troque-em-producao")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", "sqlite:///agenda.db"
)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AGENDA_API_URL = os.environ.get(
        "AGENDA_API_URL", "http://localhost:5000/api/agendamentos"
    )
    AGENDA_API_TIMEOUT = int(os.environ.get("AGENDA_API_TIMEOUT", "5"))