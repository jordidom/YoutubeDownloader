from flask import Flask, request, render_template_string
from pytube import YouTube
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    with open('index.html', 'r') as file:
        html_content = file.read()
    return render_template_string(html_content)

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form['url']
    try:
        descargar_video(url, 'descargas')
        return 'Video descargado exitosamente!'
    except Exception as e:
        return f'Error al descargar el video: {e}'

def descargar_video(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    try:
        yt = YouTube(url)
        print(f"Descargando vídeo: {yt.title} ...")
        yt.streams.get_highest_resolution().download(output_path=output_path)
        print(f"{yt.title} descargado exitosamente!")
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(debug=True)
