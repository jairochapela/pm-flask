from mysql.connector import connect, Error
from flask import Flask, redirect
from flask import render_template

def conexion_bd():
    return connect(host="127.0.0.1", user='jairo', password='aaa', database='xestorproxectos')

app = Flask(__name__)


@app.route("/")
def principal():
    return redirect("/proxectos")

@app.get("/proxectos")
def listar_proxectos():
    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute("SELECT id,nome,inicio,fin FROM proxectos")
    proxectos = cursor.fetchall()
    return render_template('lista_proxectos.html', proxectos=proxectos)


@app.get("/proxectos/<id>")
def detalle_proxecto(id):
    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute("SELECT id,nome,descricion,inicio,fin FROM proxectos WHERE id = %s", (id,))
    proxecto = cursor.fetchone()
    p_id,nome,descricion,inicio,fin = proxecto
    descricion = descricion.decode('utf-8')

    cursor.execute("SELECT id,nome,inicio,vencimento,fin FROM tarefas WHERE proxecto_id = %s", (id,))
    tarefas = cursor.fetchall()

    cursor.execute("SELECT participacion.persoa_id AS id,persoas.nome AS nome FROM participacion JOIN persoas ON participacion.persoa_id = persoas.id WHERE proxecto_id = %s", (id,))
    persoas = cursor.fetchall()

    return render_template('detalle_proxecto.html', id=p_id, nome=nome, descricion=descricion, inicio=inicio, fin=fin, tarefas=tarefas, persoas=persoas)


@app.get("/persoas/<id>")
def detalle_persoa(id):
    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute("SELECT id,nome,codigo FROM persoas WHERE id = %s", (id,))
    proxecto = cursor.fetchone()
    p_id,nome,codigo = proxecto

    cursor.execute("""
        SELECT tarefas.id,tarefas.nome,tarefas.inicio,tarefas.vencimento FROM asignacions
        JOIN tarefas ON asignacions.tarefa_id = tarefas.id
        WHERE persoa_id = %s AND fin IS NULL
        """, (id,))
    tarefas = cursor.fetchall()

    return render_template('detalle_persoa.html', id=p_id, nome=nome, codigo=codigo, tarefas=tarefas)


@app.get("/tarefas/<id>")
def detalle_tarefa(id):
    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute("SELECT id,nome,inicio,fin,vencimento FROM tarefas WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    p_id,nome,inicio,fin,vencimento = tarefa

    cursor.execute("""
        SELECT asignacions.persoa_id AS id,persoas.nome AS nome FROM asignacions
        JOIN persoas ON asignacions.persoa_id = persoas.id
        WHERE tarefa_id = %s
        """, (id,))
    persoas = cursor.fetchall()


    cursor.execute("""
        SELECT intervencions.id,persoas.nome,inicio,fin FROM intervencions
        JOIN persoas ON intervencions.persoa_id = persoas.id
        WHERE tarefa_id = %s
        """, (id,))
    intervencions = cursor.fetchall()

    return render_template('detalle_tarefa.html', id=p_id, nome=nome, inicio=inicio, fin=fin, vencimento=vencimento, persoas=persoas, intervencions=intervencions)

@app.post("/tarefas/<id>/completar")
def completar_tarefa(id):
    connection = conexion_bd()
    cursor = connection.cursor()
    cursor.execute("UPDATE tarefas SET fin=NOW() WHERE id = %s", (id,))
    connection.commit()
    return redirect("/tarefas/{0}".format(id))