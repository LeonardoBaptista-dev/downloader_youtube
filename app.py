from flask import Flask, render_template, request, send_file, url_for
from pytube import YouTube
import os

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'

DOWNLOADS_DIR = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOADS_DIR):
    os.mkdir(DOWNLOADS_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        formato = request.form['formato']
        yt = YouTube(url)
        if formato == 'mp3':
            arquivo = yt.streams.filter(only_audio=True).first().download(DOWNLOADS_DIR)
            novo_arquivo = os.path.join(DOWNLOADS_DIR, arquivo.split('/')[-1].split('.')[0] + '.mp3')
            os.rename(arquivo, novo_arquivo)
            resultado = f'<a href="{url_for("download", filename=novo_arquivo.split("/")[-1])}">Download MP3</a>'
        else:
            arquivo = yt.streams.filter(res='1080p').first().download(DOWNLOADS_DIR)
            resultado = f'<video controls src="{url_for("static", filename=arquivo.split("/")[-1])}"></video>'
        return render_template('index.html', resultado=resultado)
    return render_template('index.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(DOWNLOADS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return f"Arquivo '{filename}' não encontrado.", 404

if __name__ == '__main__':
    app.run(debug=True)
