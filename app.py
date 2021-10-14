import os
from flask import flash, render_template
from flask.app import Flask

app =Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/buscarcita')
def buscarcita():
    return render_template("buscarcita.html")

@app.route('/mostrarcita')
def mostrarcita():
    return render_template("mostrarcita.html")

@app.route('/citas')
def listarcitas():
    return render_template("listarcitas.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/perfil')
def verperfil():
    return render_template("perfil.html")

@app.route('/editarperfil')
def editarperfil():
    return render_template("editar_perfil.html")




