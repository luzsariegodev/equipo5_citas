from flask import Flask, g, render_template, redirect, session
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import AnyOf, InputRequired, Length, Email, EqualTo, NumberRange
import sqlite3
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"

def db():
    con = sqlite3.connect("bdsprint4.db")
    return con

class login_form(FlaskForm):
    username = StringField('username', validators=[InputRequired(message='El usuario es requerido'), Length(min=5, max=100, message='El usuario debe tener entre 5 y 100 caracteres')])
    password = PasswordField('password', validators=[InputRequired('Contraseña es requerida')])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = login_form()    
    if form.validate_on_submit():
        con = db()
        cur = con.cursor()
        hash_func = hashlib.sha256()
        encoded_pwd = form.password.data.encode()
        hash_func.update(encoded_pwd)
        login_statement = "SELECT usuarios.cedula, usuarios.tipousuario FROM usuarios where usuarios.usuario=? and usuarios.password= ?"
        cur.execute(login_statement, [form.username.data, hash_func.hexdigest()])
        usuario = cur.fetchone()
        cur.close()
        if usuario:
            print(usuario)
            session['user_id'] = usuario[0]
            session['user_tipousuario'] = usuario[1]
            return redirect(url_for('listarcitas'))  
        else:
            return redirect(url_for('index'))     
    return render_template('index.html', form=form)

class registro_form(FlaskForm):
    nombre_registro = StringField('nombre', validators=[InputRequired(message='El campo nombre es requerido'), Length(min=5, max=100, message='El campo nombre debe tener entre 5 y 100 caracteres')])
    apellido_registro = StringField('apellido', validators=[InputRequired(message='El campo apellido es requerido'), Length(min=5, max=100, message='El campo apellido debe tener entre 5 y 100 caracteres')])
    cedula_registro = StringField('cedula', validators=[InputRequired(message='El campo cedula es requerido'), Length(min=5, max=100, message='El campo cedula debe tener entre 5 y 100 caracteres')])
    correo_registro = StringField('correo', validators=[InputRequired(message='El campo correo es requerido'), Length(min=5, max=100, message='El campo correo debe tener entre 5 y 100 caracteres')])
    usuario_registro = StringField('usuario', validators=[InputRequired(message='El campo usuario es requerido'), Length(min=5, max=100, message='El campo usuario debe tener entre 5 y 100 caracteres')])
    password_registro = PasswordField('password', validators=[InputRequired('Contraseña es requerida'), EqualTo('password_repeat_registro', message='Las claves deben coincidir')])
    password_repeat_registro = PasswordField('password_repeat',validators=[InputRequired(message='Repite la clave')])
    genero_registro = SelectField(u'Género', choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])


@app.route('/registro', methods=['GET','POST'])
def registro():
    form = registro_form()
    con = db()
    cur = con.cursor()
    if form.validate_on_submit():
        hash_func = hashlib.sha256()
        encoded_pwd = form.password_registro.data.encode()
        hash_func.update(encoded_pwd)
        user_statement = "INSERT INTO USUARIOS (NOMBRE,APELLIDO,CEDULA,GENERO,CORREO,USUARIO,PASSWORD,TIPOUSUARIO) VALUES (?,?,?,?,?,?,?,'paciente')"
        cur.execute(user_statement, [
            form.nombre_registro.data, 
            form.apellido_registro.data, 
            form.cedula_registro.data,
            form.correo_registro.data, 
            form.usuario_registro.data, 
            hash_func.hexdigest()
        ])       
        paciente_statement = "INSERT INTO PACIENTES (CEDULA, EPS) VALUES (?,'');"
        cur.execute(paciente_statement, [form.cedula_registro.data])
        cur.close()
        con.commit()
        return redirect(url_for('index'))
    return render_template('registro.html', form=form)

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


@app.before_request
def check_session():
    user_id = session.get('user_id')
    user_tipousuario = session.get('user_tipousuario')
    exceptions = ['/', '/registro', '/logout']

    if request.path.find('static') > 0 or request.path.find('favicon') > 0 or request.path in exceptions or request.method != 'GET':
        pass
    else:
        if not user_id:
            return redirect(url_for('/'))





