
from flask import redirect, render_template, request, flash, session
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def inicio():
    return redirect('/home')

@app.route("/registro")
def registro():

    # if 'email' in session:
    #     flash('Ya estás LOGEADO!', 'warning')
    #     return redirect('/audios')

    return render_template("register.html")

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():

    if not Usuario.validar(request.form):
        return redirect('/registro')

    pass_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pass_hash,
    }

    resultado = Usuario.save(data)

    if not resultado:
        flash("error al crear el usuario", "error")
        return redirect("/registro")

    flash("Usuario creado correctamente", "success")
    return redirect("/login")

@app.route("/login")
def login():

    # if 'email' in session:
    #     flash('Ya estás LOGEADO!', 'warning')
    #     return redirect('/audios')

    return render_template("log.html")


@app.route("/procesar_login", methods=["POST"])
def procesar_login():

    usuario = Usuario.buscar(request.form['identificacion'])

    if not usuario:
        flash("Correo/Clave Invalidas", "error")
        return redirect("/login")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Correo/Clave Invalidas", "error")
        return redirect("/login")

    session['first_name'] = usuario.first_name
    session['email'] = usuario.email
    session['last_name'] = usuario.last_name
    
    return redirect('/audios')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')