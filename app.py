from sqlalchemy import create_engine, text
from flask import Flask, redirect
from flask import render_template
from flask_dotenv import DotEnv
import os

app = Flask(__name__)
env = DotEnv(app)
dbengine = None

def conexion_bd():
    global dbengine
    if not dbengine:
        dbengine = create_engine('mysql+pymysql://{0}:{1}@{2}:3306/{3}'.format(os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'], os.environ['DB_NAME']))
    return dbengine.connect()


@app.route("/")
def principal():
    return redirect("/proxectos")

@app.get("/proxectos")
def listar_proxectos():
    c = conexion_bd()
    r = c.execute("SELECT id,nome,inicio,fin FROM proxectos")
    proxectos = r.fetchall()
    return render_template('lista_proxectos.html', proxectos=proxectos)


@app.get("/proxectos/<id>")
def detalle_proxecto(id):
    c = conexion_bd()
    r = c.execute("SELECT id,nome,descricion,inicio,fin FROM proxectos WHERE id = %s", (id,))
    proxecto = r.fetchone()
    p_id,nome,descricion,inicio,fin = proxecto

    r = c.execute("SELECT id,nome,inicio,vencimento,fin FROM tarefas WHERE proxecto_id = %s", (id,))
    tarefas = r.fetchall()

    c.execute("SELECT participacion.persoa_id AS id,persoas.nome AS nome FROM participacion JOIN persoas ON participacion.persoa_id = persoas.id WHERE proxecto_id = %s", (id,))
    persoas = r.fetchall()

    return render_template('detalle_proxecto.html', id=p_id, nome=nome, descricion=descricion, inicio=inicio, fin=fin, tarefas=tarefas, persoas=persoas)


@app.get("/persoas/<id>")
def detalle_persoa(id):
    c = conexion_bd()
    r = c.execute("SELECT id,nome,codigo FROM persoas WHERE id = %s", (id,))
    proxecto = r.fetchone()
    p_id,nome,codigo = proxecto

    r = c.execute("""
        SELECT tarefas.id,tarefas.nome,tarefas.inicio,tarefas.vencimento FROM asignacions
        JOIN tarefas ON asignacions.tarefa_id = tarefas.id
        WHERE persoa_id = %s AND fin IS NULL
        """, (id,))
    tarefas = r.fetchall()

    return render_template('detalle_persoa.html', id=p_id, nome=nome, codigo=codigo, tarefas=tarefas)


@app.get("/tarefas/<id>")
def detalle_tarefa(id):
    c = conexion_bd()
    r = c.execute("SELECT id,nome,inicio,fin,vencimento FROM tarefas WHERE id = %s", (id,))
    tarefa = r.fetchone()
    p_id,nome,inicio,fin,vencimento = tarefa

    r = c.execute("""
        SELECT asignacions.persoa_id AS id,persoas.nome AS nome FROM asignacions
        JOIN persoas ON asignacions.persoa_id = persoas.id
        WHERE tarefa_id = %s
        """, (id,))
    persoas = r.fetchall()


    r = c.execute("""
        SELECT intervencions.id,persoas.nome,inicio,fin FROM intervencions
        JOIN persoas ON intervencions.persoa_id = persoas.id
        WHERE tarefa_id = %s
        """, (id,))
    intervencions = r.fetchall()

    return render_template('detalle_tarefa.html', id=p_id, nome=nome, inicio=inicio, fin=fin, vencimento=vencimento, persoas=persoas, intervencions=intervencions)

@app.post("/tarefas/<id>/completar")
def completar_tarefa(id):
    c = conexion_bd()
    c.execute("UPDATE tarefas SET fin=NOW() WHERE id = %s", (id,))
    return redirect("/tarefas/{0}".format(id))


if __name__ == '__main__':
    app.run()