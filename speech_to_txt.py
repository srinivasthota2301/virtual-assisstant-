# speech_to_txt.py
import speech_recognition as sr

def speech_to_txt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        voice_data = r.recognize_google(audio).lower()  # Fixed typo and added lower()
        print(f"User said: {voice_data}")
        return voice_data
    except sr.UnknownValueError:
        print("Could not understand audio")
        return "Could not understand"
    except sr.RequestError:
        print("Service is down")
        return "Service error"
    