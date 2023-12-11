from flask import Flask, request, render_template, Response
from pytube import YouTube
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form['url']
    try:
        video_stream_url = obtener_url_directo(url)
        return descargar_video(video_stream_url)
    except Exception as e:
        return f'Error al obtener el enlace de descarga: {e}'

def obtener_url_directo(url):
    yt = YouTube(url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    return video_stream.url

def descargar_video(video_stream_url):
    try:
        response = requests.get(video_stream_url, stream=True)
        content_type = response.headers.get('content-type')
        content_length = response.headers.get('content-length', 0)

        def generate():
            for chunk in response.iter_content(chunk_size=4096):
                yield chunk

        return Response(generate(), content_type=content_type, headers={"Content-Disposition": "attachment; filename=video.mp4", "Content-Length": content_length})
    except Exception as e:
        return f'Error en la descarga del video: {e}'

if __name__ == '__main__':
    app.run(debug=True)
