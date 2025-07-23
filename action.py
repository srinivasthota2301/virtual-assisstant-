"""import txt_to_speech
import speech_to_txt
import datetime
import webbrowser


def Action(data):
    user_data=speech_to_txt.speech_to_txt()

    if"what is your Name" in user_data:
        txt_to_speech.text_to_speech("My name is virtual assistant")
        return "My name is virtual assistant"
    elif"hello" in user_data or "hye" in user_data:
        txt_to_speech.text_to_speech("Hello,boss How can i assist you today?? ")
        return "Hello,boss How can i assist you today?? "

    elif "goodmorning" in user_data:
        txt_to_speech.text_to_speech("Good Morning Boss..")
        return "Good Morning Boss.."

    elif"time now" in user_data:
        current_time=  datetime.datetime.now()
        Time=(str)(current_time)+"Hour:",(str)(current_time.minute)+"Minute"
        txt_to_speech.text_to_speech(Time)
        return Time

    elif "shutdown" in user_data:
        txt_to_speech.text_to_speech("ok Sir")

    elif "play music" in user_data:
        webbrowser.open("https://spotify.com/")
        txt_to_speech.text_to_speech("spotify.com is now ready for you")

    elif"y0utube" in user_data:
       webbrowser.open("https://youtube.com/")
       txt_to_speech.text_to_speech("youtube.com id ready for you")


    
    elif"open google" in user_data:
        webbrowser.open("https://google.com/")
        txt_to_speech.text_to_speech("google.com id ready for you")

    else:
        txt_to_speech.text_to_speech("I'm not able to understand")"""

"""
import datetime
import webbrowser
from txt_to_speech import text_to_speech

class Assistant:
    def __init__(self):
        self.name = "Virtual Assistant"
        
    def process_command(self, command):
        if not command or command == "Could not understand" or command == "Service error":
            return "I couldn't understand that. Could you please repeat?"
            
        command = command.lower()
        
        if "what is your name" in command:
            response = f"My name is {self.name}"
        elif any(word in command for word in ["hello", "hi", "hey"]):
            response = "Hello! How can I assist you today?"
        elif "good morning" in command:
            response = "Good morning! How may I help you?"
        elif "good evening" in command:
            response = "Good evening! How may I help you?"
        elif "time" in command:
            current_time = datetime.datetime.now()
            response = f"The current time is {current_time.hour:02d}:{current_time.minute:02d}"
        elif "play music" in command:
            webbrowser.open("https://spotify.com/")
            response = "Opening Spotify for you"
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com/")
            response = "Opening YouTube for you"
        elif "open google" in command:
            webbrowser.open("https://google.com/")
            response = "Opening Google for you"
        
        elif "open instagram" in command:
            webbrowser.open("https://instagram.com/")
            response = "Opening Google for you"
        elif "shutdown my system" in command:
            response = "Shutting down. Goodbye!"
        elif "restart my system " in command:
            response="restarting the system "
        else:
            response = "I'm not sure how to help with that yet"
            
        text_to_speech(response)
        return response"""

# action.py
import datetime
import webbrowser
import os
import subprocess
from txt_to_speech import text_to_speech

class Assistant:
    def __init__(self):
        self.name = "Virtual Assistant"
        self.app_paths = {
            'calculator': 'calc.exe',
            'notepad': 'notepad.exe',
            'paint': 'mspaint.exe',
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'explorer': 'explorer.exe',
            'settings': 'ms-settings:',
            'control panel': 'control',
            'task manager': 'taskmgr.exe'
        }
        
        self.websites = {
            'google': 'https://google.com',
            'youtube': 'https://youtube.com',
            'spotify': 'https://spotify.com',
            'instagram': 'https://instagram.com',
            'facebook': 'https://facebook.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'gmail': 'https://gmail.com'
        }
        
    def open_application(self, app_name):
        """Try to open a system application"""
        try:
            app_name = app_name.lower()
            if app_name in self.app_paths:
                subprocess.Popen(self.app_paths[app_name])
                return f"Opening {app_name}"
            else:
                return f"Sorry, I don't know how to open {app_name}"
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"

    def open_website(self, site_name):
        """Open a website in the default browser"""
        try:
            site_name = site_name.lower()
            if site_name in self.websites:
                webbrowser.open(self.websites[site_name])
                return f"Opening {site_name}"
            else:
                # Try to open as URL if it's not in our predefined list
                if not site_name.startswith(('http://', 'https://')):
                    site_name = 'https://' + site_name
                webbrowser.open(site_name)
                return f"Opening {site_name}"
        except Exception as e:
            return f"Error opening {site_name}: {str(e)}"

    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now()
        return f"The current time is {current_time.strftime('%I:%M %p')}"

    def process_command(self, command):
        """Process user commands"""
        if not command or command == "Could not understand" or command == "Service error":
            return "I couldn't understand that. Could you please repeat?"
            
        command = command.lower()
        
        # Basic commands
        if "what is your name" in command:
            response = f"My name is {self.name}"
        
        # Greetings
        elif any(word in command for word in ["hello", "hi", "hey", "hye"]):
            response = "Hello! How can I assist you today?"
        elif "how are you?" in command:
            response = "i'm good! what about you? ,how can i assist you today??"
        elif "good morning" in command:
            response = "Good morning! How may I help you?"
            
        # Time related
        elif any(phrase in command for phrase in ["time now", "current time", "what time"]):
            response = self.get_time()
            
        # Open websites
        elif "open" in command and any(site in command for site in self.websites.keys()):
            site = next(site for site in self.websites.keys() if site in command)
            response = self.open_website(site)
            
        # Open applications
        elif "open" in command and any(app in command for app in self.app_paths.keys()):
            app = next(app for app in self.app_paths.keys() if app in command)
            response = self.open_application(app)
            
        # Play music (opens Spotify)
        elif "play music" in command:
            response = self.open_website("spotify")
            
        # Shutdown command
        elif "shutdown" in command:
            response = "Shutting down. Goodbye!"
            
        # Generic open command
        elif "open" in command:
            # Extract what to open from the command
            try:
                to_open = command.split("open ")[-1].strip()
                # Try as application first
                app_response = self.open_application(to_open)
                if "Sorry" in app_response:
                    # If not an app, try as website
                    response = self.open_website(to_open)
                else:
                    response = app_response
            except:
                response = "I'm not sure how to open that"
        
        else:
            response = "I'm not sure how to help with that yet"
            
        # Convert response to speech
        text_to_speech(response)
        return response

