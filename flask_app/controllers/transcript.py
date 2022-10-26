
from flask import redirect, render_template, request, flash, send_file, session, url_for
from flask_app import app
from werkzeug.utils import secure_filename 
import os
from random import sample
from pydub import AudioSegment
from flask_app.models.registro import Registro
import whisper
import pytube

@app.route("/audios")
def index():
    if 'email' not in session:
        flash('Primero tienes que logearte', 'error')
        return redirect('/login')

    registros= Registro.get_by_id(session['id_usuario'])
    total_registros = False
    if registros is None:
        cantidad_Registros = 0
        return render_template('/conversor.html', total_registros=total_registros, cantidad_Registros=cantidad_Registros)

    cantidad_Registros = len(registros)
    if cantidad_Registros >= 5:
        total_registros = True
        return render_template('/conversor.html', total_registros=total_registros, cantidad_Registros=cantidad_Registros)

    return render_template("/conversor.html", cantidad_Registros=cantidad_Registros, total_registros=total_registros,)


@app.route('/registrar_archivo_wav', methods=['GET', 'POST'])
def wav_to_text():
    if 'email' not in session:
        flash('Registrate/inicia session', 'error')
        return redirect('/login')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','error')
            return redirect('/audios')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' :
            flash('No selected file', 'error')
            return redirect('/audios')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('flask_app/static/archivos', filename))

        model = whisper.load_model("small")
        result = model.transcribe(f'flask_app/static/archivos/{filename}')

        print("La espera dependerá del largo del audio. de 1-5 min.")
        file = open("flask_app/textos/nueva_grabacion.txt", 'w')
        file.write(result["text"])
        file.close()
       
        data = {
            'usuarios_id': session['id_usuario'],
            'registro': 'nueva_grabacion.txt'
        }   
        Registro.save(data)
        return redirect(url_for("download"))
      
  


@app.route('/registrar_youtube', methods=['GET', 'POST'])
def youtube_to_text():

    if 'email' not in session:
        flash('Registrate/inicia session', 'error')
        return redirect('/login')

    if request.method == 'POST':
        # check if the post request has the file part
        if len(request.form['youtube']) < 1:
            flash('No file part','error')
            return redirect('/audios')

        if 'youtube' not in request.form:
            flash('No file part','error')
            return redirect('/audios')

        file = request.form['youtube']
        youtubeVideo = pytube.YouTube(file)
        audio = youtubeVideo.streams.get_audio_only()
        audio.download(filename='flask_app/static/archivos/tmp.mp4')
        model = whisper.load_model("small")
        result = model.transcribe('flask_app/static/archivos/tmp.mp4')

        file = open("flask_app/textos/youtube_grabacion.txt", 'w')
        file.write(result["text"])
        file.close()

        data = {
            'usuarios_id': session['id_usuario'],
            'registro': 'youtube_grabacion.txt'
        }   
        Registro.save(data)
        return redirect(url_for("download"))

@app.route('/registrar_mp4', methods=['GET', 'POST'])
def mp4_to_text():
    if 'email' not in session:
        flash('Registrate/inicia session', 'error')
        return redirect('/login')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'mp4' not in request.files:
            flash('No mp4 part','error')
            return redirect('/audios')
        file = request.files['mp4']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' :
            flash('No selected mp4', 'error')
            return redirect('/audios')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('flask_app/static/archivos', filename))

        model = whisper.load_model("small")
        result = model.transcribe(f'flask_app/static/archivos/{filename}')

        print("La espera dependerá del largo del audio. de 1-5 min.")
        file = open("flask_app/textos/new_mp4.txt", 'w')
        file.write(result["text"])
        file.close()

        data = {
            'usuarios_id': session['id_usuario'],
            'registro': 'new_mp4.txt'
        }   
        Registro.save(data)
        return redirect(url_for("download"))

@app.route('/registrar_m4a', methods=['GET', 'POST'])
def m4a_to_text():
    if 'email' not in session:
        flash('Registrate/inicia session', 'error')
        return redirect('/login')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'm4a' not in request.files:
            flash('No m4a part','error')
            return redirect('/audios')
        file = request.files['m4a']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '' :
            flash('No selected m4a', 'error')
            return redirect('/audios')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('flask_app/static/archivos', filename))

        model = whisper.load_model("small")
        result = model.transcribe(f'flask_app/static/archivos/{filename}')

        print("La espera dependerá del largo del audio. de 1-5 min.")
        file = open("flask_app/textos/new_m4a.txt", 'w')
        file.write(result["text"])
        file.close()

        data = {
            'usuarios_id': session['id_usuario'],
            'registro': 'new_m4a.txt'
        }   
        Registro.save(data)
        return redirect(url_for("download"))

@app.route('/download')
def download():
    registros= Registro.get_by_id(session['id_usuario'])
    primera= Registro.primera(session['id_usuario'])
  
    total_registros = False
    cantidad_Registros = len(registros)
    if cantidad_Registros >= 5:
        total_registros = True
        return render_template('/download.html', total_registros=total_registros, cantidad_Registros=cantidad_Registros, primera=primera, registros=registros)

    if 'email' not in session:
        flash('Registrate/inicia session', 'error')
        return redirect('/login')
    return render_template('/download.html', cantidad_Registros=cantidad_Registros, registros=registros, primera=primera)

@app.route('/downloading/<name>')
def downloadFile(name):
   
    path = f"textos/{name}"
    return send_file(path, as_attachment=True)

