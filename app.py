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
    return render_template('detalle_proxecto.html', id=p_id, nome=nome, descricion=descricion, inicio=inicio, fin=fin)