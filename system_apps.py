# system_apps.py
import os
import subprocess
import platform

class SystemApps:
    def __init__(self):
        self.system = platform.system()

    def open_app(self, app_name):
        app_name = app_name.lower().strip()
        
        # Dictionary of Windows apps and their commands
        windows_apps = {
            "settings": "ms-settings:",
            "store": "ms-windows-store:",
            "calculator": "calc.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "file explorer": "explorer.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "word": "WINWORD.EXE",
            "excel": "EXCEL.EXE",
            "powerpoint": "POWERPNT.EXE",
            "outlook": "OUTLOOK.EXE",
            "edge": "msedge.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe"
        }

        # Dictionary of macOS apps
        mac_apps = {
            "settings": "System Preferences.app",
            "calculator": "Calculator.app",
            "finder": "Finder.app",
            "terminal": "Terminal.app",
            "safari": "Safari.app"
        }

        # Dictionary of Linux apps
        linux_apps = {
            "settings": "gnome-control-center",
            "calculator": "gnome-calculator",
            "files": "nautilus",
            "terminal": "gnome-terminal"
        }

        try:
            if self.system == "Windows":
                if app_name in windows_apps:
                    if app_name in ["settings", "store"]:
                        subprocess.run(["start", windows_apps[app_name]], shell=True)
                    else:
                        subprocess.Popen(windows_apps[app_name], shell=True)
                    return f"Opening {app_name}..."
                else:
                    return f"Sorry, I don't know how to open {app_name}"
                    
            elif self.system == "Darwin":  # macOS
                if app_name in mac_apps:
                    subprocess.run(["open", "-a", mac_apps[app_name]])
                    return f"Opening {app_name}..."
                else:
                    return f"Sorry, I don't know how to open {app_name}"
                    
            elif self.system == "Linux":
                if app_name in linux_apps:
                    subprocess.Popen([linux_apps[app_name]])
                    return f"Opening {app_name}..."
                else:
                    return f"Sorry, I don't know how to open {app_name}"
            
            else:
                return f"Unsupported operating system: {self.system}"
                    
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    
    def open_file(self, file_path):
        try:
            file_path = os.path.expanduser(file_path)  # Expand ~ to user home directory
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
                
            if self.system == "Windows":
                os.startfile(os.path.normpath(file_path))
            elif self.system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            elif self.system == "Linux":
                subprocess.run(["xdg-open", file_path])
            else:
                return f"Unsupported operating system: {self.system}"
                
            return f"Opening {file_path}..."
        except Exception as e:
            return f"Error opening file: {str(e)}"
    
    def open_folder(self, folder_path):
        try:
            folder_path = os.path.expanduser(folder_path)  # Expand ~ to user home directory
            if not os.path.exists(folder_path):
                return f"Folder not found: {folder_path}"
                
            if self.system == "Windows":
                subprocess.run(['explorer', os.path.normpath(folder_path)], shell=True)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            elif self.system == "Linux":
                subprocess.run(["xdg-open", folder_path])
            else:
                return f"Unsupported operating system: {self.system}"
                
            return f"Opening folder: {folder_path}"
        except Exception as e:
            return f"Error opening folder: {str(e)}"+