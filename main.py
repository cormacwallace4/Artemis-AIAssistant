import os
import time
import pyaudio
import speech_recognition as sr
from google.cloud import texttospeech
import openai
import io
from pydub import AudioSegment
from pydub.playback import play

from google.oauth2.service_account import Credentials

# Create credentials from the JSON key file
credentials = Credentials.from_service_account_file('/Users/cormac/desktop/artemis/origin-388215-458f8798b045.json')

# Initialize the Text-to-Speech client with the credentials
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Define the voice parameters. Here, you're using an English (en-GB) male voice
voice = texttospeech.VoiceSelectionParams(
    language_code="en-GB",
    name="en-GB-Neural2-D",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
)

# Define the audio configuration
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

api_key = "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"
openai.api_key = api_key

guy = ""

while True:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said

                if "Artemis" in said:
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    print(new_string)
                    instruction = "Please provide a response that is no longer than 50 words."
                    complete_message = f"{instruction} {new_string}"
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                              messages=[{"role": "user", "content": complete_message}])
                    text = completion.choices[0].message.content

                    # Using Google Cloud Text-to-Speech to get audio data
                    synthesis_input = texttospeech.SynthesisInput(text=text)
                    response = client.synthesize_speech(
                        input=synthesis_input, voice=voice, audio_config=audio_config
                    )

                    # Instead of saving to file, load audio directly into pydub
                    audio_stream = io.BytesIO(response.audio_content)
                    audio_segment = AudioSegment.from_mp3(audio_stream)
                    play(audio_segment)

            except Exception as e:
                print("Exception", e)

        return said

    if "thanks" in guy:
        break

    get_audio()
