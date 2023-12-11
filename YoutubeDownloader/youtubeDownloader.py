from flask import Flask, request, render_template, redirect
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form['url']
    try:
        video_url = obtener_url_directo(url)
        return redirect(video_url)
    except Exception as e:
        return f'Error al obtener el enlace de descarga: {e}'

def obtener_url_directo(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    return video_stream.url

if __name__ == '__main__':
    app.run(debug=True)
