# Controller de autenticacao - entrar, criar conta e sair.
# Estas rotas ficam FORA da protecao: sem elas ninguem entraria.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from models import usuario
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO

senha_hash = generate_password_hash("prova123")
confere = check_password_hash (senha_hash, "prova123")

auth_bp = Blueprint("auth", __name__)

#item 6
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        UsuarioDAO.buscar_por_email(request.form["email"])
        # Pega o email do formulário, remove espaços e converte em minúsculas
        email = request.form['email'].strip().lower()
        senha = request.form['senha']

        if Usuario and check_password_hash(Usuario.senha_hash, request.form["senha"]):
            session["usuario_id"] = Usuario.id
            session["usuario_nome"] = Usuario.nome
            return redirect(url_for("palestrante.index"))
        
        if autenticar_usuario(email, senha):
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("palestrante.index"))
        else:
            flash("Email ou senha incorretos. Por favor, tente novamente.", "error")

    return render_template("login.html")

@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    #Item 6
    if request.method == "POST":
        email = request.form['email'].strip().lower()
        senha = request.form['senha']
        nome = request.form['nome']

        if UsuarioDAO.buscar_por_email(request.form["email"]):
            flash("Ja existe uma conta com este e-mail.")
            return render_template("cadastro.html")

        usuario = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            senha_hash=generate_password_hash(request.form["senha"])
        )
        UsuarioDAO.salvar(usuario)
        flash("Conta criada. Faca login para continuar.")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html")

def autenticar_usuario(email, password):
    usuario = UsuarioDAO.buscar_por_email(request.form["email"])
    if usuario and check_password_hash(usuario.senha_hash, password):
        session["usuario_id"] = usuario.id
        session["usuario_perfil"] = usuario.perfil
        return True
    return False

@auth_bp.route("/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("auth.login"))
