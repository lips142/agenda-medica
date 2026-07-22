from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("agenda.index"))

    if request.method == "POST":
        identificador = request.form.get("identificador", "").strip()
        senha = request.form.get("senha", "")

        if not identificador or not senha:
            flash("Usuário ou senha inválidos.", "error")
            return render_template("login.html")

        user = User.query.filter(
            (User.username == identificador) | (User.email == identificador)
        ).first()

        if user is None or not user.check_password(senha):
            flash("Usuário ou senha inválidos.", "error")
            return render_template("login.html")

        login_user(user)
        return redirect(url_for("agenda.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))