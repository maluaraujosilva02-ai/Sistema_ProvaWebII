# Controller de PAGINAS - todas as rotas daqui respondem HTML ou
# redirecionamento.

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask import session
from models.palestrante import Palestrante
from dao.palestrante_dao import PalestranteDAO

palestrante_bp = Blueprint("palestrante", __name__)

@palestrante_bp.before_request
def exigir_login():
    if 'usuario_id' not in session:
        flash("Você precisa estar logado para acessar esta página.")
        return redirect(url_for('autenticacao.login'))
    
def converter_vagas_para_inteiro(texto):
    texto = texto.strip()
    return int(texto) if texto.isdigit() else None

# Listagem (GET) e cadastro (POST) na mesma rota
@palestrante_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        palestrante = Palestrante(
            nome=request.form["nome"],
            tema=request.form["tema"],
            minutos=request.form["minutos"]
        )
        PalestranteDAO.salvar(palestrante)
        flash("Palestrante cadastrado.")
        return redirect(url_for("palestrante.index"))

    # Item 3
    if "visitas" not in session:
        session["visitas"] = 0
    session["visitas"] += 1

    return render_template("index.html", palestrantes=PalestranteDAO.listar())


# Edicao - GET mostra o formulario preenchido
@palestrante_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    palestrante = PalestranteDAO.buscar_por_id(id)
    #item 4
    if palestrante is None:          # id inexistente -> pagina 404
        abort(404)

    if request.method == "POST":
        PalestranteDAO.atualizar(
            palestrante,
            nome=request.form["nome"],
            data=request.form["data"],
            local=request.form["local"],
            vagas=converter_vagas_para_inteiro(request.form["vagas"]),
        )
        flash("Palestrante atualizado.")
        return redirect(url_for("palestrante.index"))

    return render_template("editar.html", palestrante=palestrante)


# Exclusao
@palestrante_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    palestrante = PalestranteDAO.buscar_por_id(id)
    PalestranteDAO.excluir(palestrante)
    flash("Palestrante excluido.")
    return redirect(url_for("palestrante.index"))
