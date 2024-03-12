from flask import *
from gtts import gTTS
import speech_recognition as sr
import moviepy.editor as mp
import os

app = Flask(__name__)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/text-to-speech')
def text_to_speech():
    return render_template('text.html')

@app.route('/speech-to-text')
def speech_to_text():
    return render_template('audio.html')

@app.route('/text-to-video')
def text_to_video():
    return render_template('video.html')


@app.route('/convert', methods=['POST'])

def convert():

    if request.method == 'POST':

        data=request.form['data']

        myfile = gTTS(text=data, lang="en", slow=False)
        myfile.save("./media/output.mp3")

    return render_template("download.html")

@app.route('/download', methods=['POST']) 
def download():

    if request.method=='POST':

        return send_file("./media/output.mp3",as_attachment=True)
    


@app.route("/speech-to-text", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('audio.html', transcript=transcript)


@app.route("/text-to-video", methods=["GET", "POST"])
def video_to_text():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        print(file)
        if file.filename == "":
            return redirect(request.url)

        if file:
            video_path = os.path.join(os.getcwd(), file.filename)
            file.save(video_path)
            clip = mp.VideoFileClip(video_path)
            transcript = clip.audio.write_audiofile("audio.wav")
            r = sr.Recognizer()

            # Load the audio file
            with sr.AudioFile("audio.wav") as source:
                data = r.record(source)

            # Convert speech to text
            transcript = r.recognize_google(data)


    return render_template('video.html', transcript=transcript)




if __name__ == '__main__':
    app.run(debug=True)
