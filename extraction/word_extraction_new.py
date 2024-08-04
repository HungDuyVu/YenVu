import speech_recognition as sr
from pydub import AudioSegment
from database.database import db
import os

# Initialize the recognizer
recognizer = sr.Recognizer()
folder_path = 'audio_new'

class Extraction():
    def save_audio_list(self):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                category = os.path.basename(root)
                file_name = file
                db.save_audio_name(file_name,category)

    def extract_content_words_by_id(self,id):
        file_name = db.get_file_name_by_id(id)
        return self.extract_content_words(file_name)
    def extract_content_words(self,file_name):
        mp3_audio_file = f"audio_new/{file_name['category']}/{file_name['name']}"
        wav_audio_file = "converted_audio.wav"

        # Convert MP3 to WAV
        audio = AudioSegment.from_mp3(mp3_audio_file)
        audio.export(wav_audio_file, format="wav")
        print('start')
        # Use the recognizer to open the WAV audio file
        with sr.AudioFile(wav_audio_file) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)

            # Listen to the audio file and store the audio data in 'audio'
            audio = recognizer.record(source)

            try:
                # Use the recognizer to convert speech to text
                text = recognizer.recognize_google(audio)
                print("Transcription: ", text)
                db.save_word_extraction(text,file_name)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def extract_all_content_words(self):
        for file in self.get_audio_list():
            self.extract_content_words((file))

extraction = Extraction()