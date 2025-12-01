# web_app.py
from flask import Flask, render_template_string, request, redirect
from urllib.parse import urlencode
import sqlite3

# Importa as funções do nosso arquivo database.py
import database

# A instância 'app' deve estar no escopo global para o Gunicorn encontrar
app = Flask(__name__)


TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Membros da Universidade</title>
  <style>
    /* Estilos CSS (mantidos do original) */
    body { font-family: Arial, sans-serif; max-width: 720px; margin: 0 auto; padding: 24px; }
    h1 { margin-bottom: 4px; }
    section { border: 1px solid #ccc; padding: 16px; margin: 12px 0; border-radius: 6px; }
    label { display: block; margin: 6px 0 2px; }
    input { width: 100%; padding: 8px; margin-bottom: 8px; box-sizing: border-box; }
    button { padding: 8px 12px; cursor: pointer; }
    .message { padding: 8px; background: #eef; border: 1px solid #aac; border-radius: 4px; margin-bottom: 12px; }
  </style>
</head>
<body>
  <h1>Membros da Universidade</h1>
  <p>Use os formularios para criar, ver, atualizar ou remover um membro.</p>
  {% if message %}
    <div class="message">{{ message }}</div>
  {% endif %}

  <section>
    <h2>Criar membro</h2>
    <form method="post" action="/create">
      <label>Nome</label>
      <input name="nome" required>
      <label>Email</label>
      <input name="email" required>
      <label>Matricula</label>
      <input name="matricula" required>
      <button type="submit">Salvar</button>
    </form>
  </section>

  <section>
    <h2>Ver membro</h2>
    <form method="get" action="/read">
      <label>Matricula</label>
      <input name="matricula" required>
      <button type="submit">Buscar</button>
    </form>
    {% if membro %}
      <p><strong>Nome:</strong> {{ membro[0] }}</p>
      <p><strong>Email:</strong> {{ membro[1] }}</p>
      <p><strong>Matricula:</strong> {{ membro[2] }}</p>
    {% endif %}
  </section>

  <section>
    <h2>Atualizar membro</h2>
    <form method="post" action="/update">
      <label>Matricula (existente)</label>
      <input name="matricula" required>
      <label>Novo nome</label>
      <input name="nome" required>
      <label>Novo email</label>
      <input name="email" required>
      <button type="submit">Atualizar</button>
    </form>
  </section>

  <section>
    <h2>Deletar membro</h2>
    <form method="post" action="/delete">
      <label>Matricula</label>
      <input name="matricula" required>
      <button type="submit">Deletar</button>
    </form>
  </section>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    matricula = request.args.get("matricula")
    message = request.args.get("message")
    membro = database.buscar_membro(matricula) if matricula else None
    return render_template_string(TEMPLATE, message=message, membro=membro)


@app.route("/create", methods=["POST"])
def create():
    nome = (request.form.get("nome") or "").strip()
    email = (request.form.get("email") or "").strip()
    matricula = (request.form.get("matricula") or "").strip()
    if not nome or not email or not matricula:
        params = {"message": "Preencha todos os campos."}
        return redirect("/?" + urlencode(params))
    try:
        database.criar_membro(nome, email, matricula)
        msg = "Membro criado com sucesso."
    except sqlite3.IntegrityError:
        msg = "Ja existe um membro com essa matricula."
    params = {"matricula": matricula, "message": msg}
    return redirect("/?" + urlencode(params))


@app.route("/read", methods=["GET"])
def read():
    # Esta rota foi mantida como estava, mas o ideal seria usar a rota "/"
    matricula = (request.args.get("matricula") or "").strip()
    membro = database.buscar_membro(matricula) if matricula else None
    msg = "Nenhum membro encontrado." if matricula and not membro else None
    return render_template_string(TEMPLATE, message=msg, membro=membro)


@app.route("/update", methods=["POST"])
def update():
    nome = (request.form.get("nome") or "").strip()
    email = (request.form.get("email") or "").strip()
    matricula = (request.form.get("matricula") or "").strip()
    if not nome or not email or not matricula:
        params = {"message": "Preencha todos os campos."}
        return redirect("/?" + urlencode(params))
    linhas = database.atualizar_membro(nome, email, matricula)
    msg = "Dados atualizados." if linhas else "Nenhum membro encontrado."
    return redirect("/?" + urlencode({"matricula": matricula, "message": msg}))


@app.route("/delete", methods=["POST"])
def delete():
    matricula = (request.form.get("matricula") or "").strip()
    if not matricula:
        params = {"message": "Matricula nao pode ser vazia."}
        return redirect("/?" + urlencode(params))
    linhas = database.deletar_membro(matricula)
    msg = "Membro removido." if linhas else "Nenhum membro encontrado."
    return redirect("/?" + urlencode({"message": msg}))

# O bloco if __name__ == "__main__": foi removido para uso com Gunicorn