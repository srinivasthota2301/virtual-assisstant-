import pyttsx3

def text_to_speech(text):
    
    engine=pyttsx3.init()
    rate=engine.getProperty('rate')
    engine.setProperty('rate','rate-70')
    engine.say(text)
    engine.runAndWait()


text_to_speech("Hello boss!!")

"""import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Set default voice
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)  # Adjust speed
    engine.say(text)
    engine.runAndWait()"""

