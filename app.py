from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

ARQUIVO = "tarefas.json"


def carregar_tarefas():
    if not os.path.exists(ARQUIVO):
        return []

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_tarefas(tarefas):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)


def gerar_id(tarefas):
    if not tarefas:
        return 1
    return max(tarefa["id"] for tarefa in tarefas) + 1


@app.route("/")
def index():
    tarefas = carregar_tarefas()
    return render_template("index.html", tarefas=tarefas)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo", "").strip()

    if titulo:
        tarefas = carregar_tarefas()
        nova_tarefa = {
            "id": gerar_id(tarefas),
            "titulo": titulo,
            "concluida": False
        }
        tarefas.append(nova_tarefa)
        salvar_tarefas(tarefas)

    return redirect(url_for("index"))


@app.route("/concluir/<int:id_tarefa>")
def concluir(id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["concluida"] = not tarefa["concluida"]
            break

    salvar_tarefas(tarefas)
    return redirect(url_for("index"))


@app.route("/remover/<int:id_tarefa>")
def remover(id_tarefa):
    tarefas = carregar_tarefas()
    tarefas = [tarefa for tarefa in tarefas if tarefa["id"] != id_tarefa]
    salvar_tarefas(tarefas)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)