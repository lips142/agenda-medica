from app import create_app
from app.extensions import db
from app.models import User


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if User.query.filter_by(username="admin").first() is None:
            usuario_teste = User(username="admin", email="admin@agendamedica.com")
            usuario_teste.set_password("admin123")
            db.session.add(usuario_teste)
            db.session.commit()
            print("Usuário de teste criado: admin / admin123")
        else:
            print("Usuário de teste já existe.")


if __name__ == "__main__":
    seed()