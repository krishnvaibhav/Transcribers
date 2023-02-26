import os
from flask import Flask, render_template, redirect, request, url_for
import soundfile as sf
import speech_recognition as sr
from deep_translator import GoogleTranslator
import math
import languages
import subprocess


app = Flask(__name__)

error = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    final = ""
    final_text = []

    if request.method == 'POST':
        file = request.files['file']
        src_lang = request.form.get('lang')
        dst_lang = request.form.get('text')

        if file:

            # Converting into wavfile
            try:
                file.save(file.filename)
                input_file = file.filename
                output_file = f"{file.filename}.wav"

                command = ['ffmpeg', '-i', input_file, output_file]

                try:
                    subprocess.run(command, check=True)
                except subprocess.CalledProcessError as error:
                    error = f"Error: {error}"
                

                max_duration = 30.0

                with sf.SoundFile(f'{file.filename}.wav') as f:
                    frames = len(f)
                    samplerate = f.samplerate
                    duration = frames / float(samplerate)

                    num_subs = math.ceil(duration / max_duration)
                    frames_per_sub = int(max_duration * samplerate)


                    for i in range(num_subs):
                        sub_frames = f.read(frames_per_sub, dtype='float32')
                        sub_filename = f"{file.filename.split('.')[0]}_part{i + 1}.wav"
                        sf.write(sub_filename, sub_frames, samplerate)
                        print(f"Sub-file {i + 1} was written to {sub_filename}")
                        
                        r = sr.Recognizer()
                        with sr.AudioFile(sub_filename) as source:
                            audio = r.record(source)
                        
                        try:
                            text = r.recognize_google(audio, language=src_lang)
                            print("Malayalam text: " + text)
                            final = GoogleTranslator(source='auto', target=dst_lang).translate(text)
                            final_text.append(final)
                        except sr.UnknownValueError:
                            error = "could not understand audio"
                        except sr.RequestError as e:
                            error = "Could not request results "
                        os.remove(sub_filename)

                os.remove(file.filename)
                os.remove(file.filename + '.wav')
                final_text = "".join(final_text)
            except :
                error = "Audio File Not supported"

            if os.path.exists(file.filename):
                os.remove(file.filename)
            return render_template('audio-to-text.html',final_text=final_text
                                   ,languages=languages.languages,dst_languages=languages.dst_languages,error=error)

    return render_template('audio-to-text.html',languages=languages.languages,dst_languages=languages.dst_languages,error=error)


if __name__ == '__main__':
    app.run(debug=True)
