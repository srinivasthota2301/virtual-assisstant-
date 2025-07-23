
"""import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import speech_to_txt
from action import Assistant
from weather import WeatherService 
from system_ops import SystemOperations
from gui import VirtualAssistantGUI, SystemApps

class EnhancedVirtualAssistantGUI(VirtualAssistantGUI):
    def __init__(self):
        super().__init__()
        self.system_ops = SystemOperations()
        
        # Add system operations frame to the main frame
        self.add_system_ops_frame()
        
    def add_system_ops_frame(self):
        # System operations frame
        sys_ops_frame = ttk.LabelFrame(self.main_frame, text="System Operations", padding="10")
        sys_ops_frame.pack(pady=10)
        
        # Buttons frame for system operations
        sys_ops_buttons_frame = ttk.Frame(sys_ops_frame)
        sys_ops_buttons_frame.pack()
        
        # Add shutdown and restart buttons
        ttk.Button(
            sys_ops_buttons_frame,
            text="Shutdown",
            command=lambda: self.execute_system_op("shutdown")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            sys_ops_buttons_frame,
            text="Restart",
            command=lambda: self.execute_system_op("restart")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            sys_ops_buttons_frame,
            text="Cancel Operation",
            command=lambda: self.execute_system_op("cancel shutdown")
        ).pack(side=tk.LEFT, padx=5)
    
    def execute_system_op(self, command):
        response = self.system_ops.process_command(command)
        if response:
            self.display_message(f"Assistant: {response}")
    
    def handle_system_command(self, command):
        # First check for system operations
        response = self.system_ops.process_command(command)
        if response:
            return response
            
        # If not a system operation, use parent class handler
        return super().handle_system_command(command)
    
    def send_message(self):
        user_input = self.input_field.get()
        if user_input:
            self.display_message(f"You: {user_input}")
            
            # Check for system operations first
            response = self.system_ops.process_command(user_input.lower())
            if response:
                self.display_message(f"Assistant: {response}")
            else:
                # Use existing message handling
                super().send_message()
    
    def listen_command(self):
        self.display_message("Assistant: Listening...")
        command = speech_to_txt.speech_to_txt()
        if command:
            self.display_message(f"You: {command}")
            
            # Check for system operations first
            response = self.system_ops.process_command(command.lower())
            if response:
                self.display_message(f"Assistant: {response}")
            else:
                # Use existing command handling
                super().listen_command()

if __name__ == "__main__":
    app = EnhancedVirtualAssistantGUI()
    app.run()"""

# enhanced_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import speech_to_txt
from action import Assistant
from weather import WeatherService 
from system_ops import SystemOperations
from gui import SystemApps
import os

class EnhancedVirtualAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Virtual Assistant")
        self.root.geometry("900x700")
        
        # Initialize components
        self.assistant = Assistant()
        self.weather_service = WeatherService()
        self.system_apps = SystemApps()
        self.system_ops = SystemOperations()
        
        self.setup_window()
        self.setup_gui()
        self.add_system_ops_frame()
        
    def setup_window(self):
        try:
            image = Image.open("background.png")
            image = image.resize((900, 700), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg="#1E1E1E")

        self.main_frame = ttk.Frame(self.root, padding="20", style='Transparent.TFrame')
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        style = ttk.Style()
        style.configure('Transparent.TFrame', background='#1E1E1E')
        
    def setup_gui(self):
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="Virtual Assistant",
            font=("Arial", 24, "bold"),
            bg='#1E1E1E',
            fg='#00FFFF'
        )
        title_label.pack(pady=20)

        # Setup all frames
        self.setup_weather_frame()
        self.setup_quick_actions_frame()
        self.setup_chat_display()
        self.setup_input_field()
        self.setup_buttons()

    def setup_weather_frame(self):
        weather_frame = ttk.LabelFrame(self.main_frame, text="Quick Weather", padding="10")
        weather_frame.pack(pady=10)
        
        weather_input_frame = ttk.Frame(weather_frame)
        weather_input_frame.pack()
        
        self.city_entry = ttk.Entry(weather_input_frame, width=30)
        self.city_entry.pack(side=tk.LEFT, padx=5)
        self.city_entry.insert(0, "Enter city name")
        
        self.city_entry.bind('<FocusIn>', self._clear_placeholder)
        self.city_entry.bind('<FocusOut>', self._restore_placeholder)
        self.city_entry.bind('<Return>', lambda e: self.quick_weather())
        
        weather_btn = ttk.Button(
            weather_input_frame,
            text="Get Weather",
            command=self.quick_weather
        )
        weather_btn.pack(side=tk.LEFT, padx=5)

    def setup_quick_actions_frame(self):
        actions_frame = ttk.LabelFrame(self.main_frame, text="Quick Actions", padding="10")
        actions_frame.pack(pady=10)
        
        actions_buttons_frame = ttk.Frame(actions_frame)
        actions_buttons_frame.pack()
        
        # Common applications buttons
        common_apps = [
            ("Calculator", "calculator"),
            ("Notepad", "notepad"),
            ("Browser", "chrome"),
            ("Files", "explorer")
        ]
        
        for app_text, app_name in common_apps:
            ttk.Button(
                actions_buttons_frame,
                text=app_text,
                command=lambda a=app_name: self.quick_open_app(a)
            ).pack(side=tk.LEFT, padx=5)
            
        # Common websites frame
        websites_frame = ttk.Frame(actions_frame)
        websites_frame.pack(pady=10)
        
        common_sites = [
            ("Google", "google"),
            ("YouTube", "youtube"),
            ("Spotify", "spotify"),
            ("Gmail", "gmail")
        ]
        
        for site_text, site_name in common_sites:
            ttk.Button(
                websites_frame,
                text=site_text,
                command=lambda s=site_name: self.quick_open_website(s)
            ).pack(side=tk.LEFT, padx=5)

    def setup_chat_display(self):
        self.chat_display = tk.Text(
            self.main_frame,
            height=15,
            width=70,
            font=("Arial", 12),
            wrap=tk.WORD,
            bg='#2D2D2D',
            fg='#00FFFF'
        )
        self.chat_display.pack(pady=20)
        
    def setup_input_field(self):
        self.input_field = ttk.Entry(
            self.main_frame,
            width=60,
            font=("Arial", 12)
        )
        self.input_field.pack(pady=10)
        self.input_field.bind('<Return>', lambda e: self.send_message())
        
    def setup_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Send", self.send_message),
            ("Speak", self.listen_command),
            ("Clear", self.clear_chat)
        ]
        
        for text, command in buttons:
            ttk.Button(
                button_frame,
                text=text,
                command=command
            ).pack(side=tk.LEFT, padx=5)

    def add_system_ops_frame(self):
        sys_ops_frame = ttk.LabelFrame(self.main_frame, text="System Operations", padding="10")
        sys_ops_frame.pack(pady=10)
        
        sys_ops_buttons_frame = ttk.Frame(sys_ops_frame)
        sys_ops_buttons_frame.pack()
        
        operations = [
            ("Shutdown", "shutdown"),
            ("Restart", "restart"),
            ("Cancel Operation", "cancel")
        ]
        
        for op_text, op_command in operations:
            ttk.Button(
                sys_ops_buttons_frame,
                text=op_text,
                command=lambda cmd=op_command: self.execute_system_op(cmd)
            ).pack(side=tk.LEFT, padx=5)

    def _clear_placeholder(self, event):
        if self.city_entry.get() == "Enter city name":
            self.city_entry.delete(0, tk.END)
            
    def _restore_placeholder(self, event):
        if not self.city_entry.get():
            self.city_entry.insert(0, "Enter city name")

    def quick_weather(self):
        city = self.city_entry.get()
        if city and city != "Enter city name":
            weather_info = self.weather_service.get_weather(city)
            self.display_message(f"Assistant: {weather_info}")
            self.city_entry.delete(0, tk.END)
            self._restore_placeholder(None)
        else:
            self.display_message("Assistant: Please enter a city name")

    def quick_open_app(self, app_name):
        response = self.assistant.open_application(app_name)
        self.display_message(f"Assistant: {response}")

    def quick_open_website(self, site_name):
        response = self.assistant.open_website(site_name)
        self.display_message(f"Assistant: {response}")

    def execute_system_op(self, command):
        response = self.system_ops.process_command(command)
        if response:
            self.display_message(f"Assistant: {response}")

    def display_message(self, message):
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        
    def clear_chat(self):
        self.chat_display.delete(1.0, tk.END)
        
    def send_message(self):
        user_input = self.input_field.get()
        if user_input:
            self.display_message(f"You: {user_input}")
            
            # Process the command
            response = self.assistant.process_command(user_input)
            self.display_message(f"Assistant: {response}")
            
            # Clear input field
            self.input_field.delete(0, tk.END)
            
    def listen_command(self):
        self.display_message("Assistant: Listening...")
        command = speech_to_txt.speech_to_txt()
        if command:
            self.display_message(f"You: {command}")
            response = self.assistant.process_command(command)
            self.display_message(f"Assistant: {response}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedVirtualAssistantGUI()
    app.run()
    

      