import os
import platform
import subprocess
import time

class SystemOperations:
    def __init__(self):
        self.system = platform.system()

    def shutdown(self, delay=10):
        """
        Shutdown the system after specified delay (in seconds)
        Returns message indicating shutdown initiation
        """
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/s", "/t", str(delay)], shell=True)
            elif self.system == "Linux":
                os.system(f"shutdown -h {delay}")
            elif self.system == "Darwin":  # macOS
                os.system(f"sudo shutdown -h +{delay//60}")  # macOS uses minutes
            else:
                return "Unsupported operating system"
            
            return f"System will shutdown in {delay} seconds. Use 'cancel shutdown' to abort."
        except Exception as e:
            return f"Error initiating shutdown: {str(e)}"

    def restart(self, delay=10):
        """
        Restart the system after specified delay (in seconds)
        Returns message indicating restart initiation
        """
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/r", "/t", str(delay)], shell=True)
            elif self.system == "Linux":
                os.system(f"shutdown -r {delay}")
            elif self.system == "Darwin":  # macOS
                os.system(f"sudo shutdown -r +{delay//60}")  # macOS uses minutes
            else:
                return "Unsupported operating system"
            
            return f"System will restart in {delay} seconds. Use 'cancel restart' to abort."
        except Exception as e:
            return f"Error initiating restart: {str(e)}"

    def cancel_shutdown(self):
        """
        Cancel pending shutdown/restart
        Returns message indicating cancellation status
        """
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/a"], shell=True)
            elif self.system in ["Linux", "Darwin"]:
                os.system("shutdown -c")
            else:
                return "Unsupported operating system"
            
            return "Shutdown/restart has been cancelled."
        except Exception as e:
            return f"Error cancelling shutdown: {str(e)}"

    def process_command(self, command):
        """
        Process system operation commands
        Returns appropriate response message
        """
        command = command.lower().strip()
        
        if "shutdown" in command:
            if "cancel" in command:
                return self.cancel_shutdown()
            else:
                return self.shutdown()
        elif "restart" in command:
            if "cancel" in command:
                return self.cancel_shutdown()
            else:
                return self.restart()
        
        return None