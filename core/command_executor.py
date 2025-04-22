# Executes specified commands

import subprocess
import shlex

class CommandExecutor:
    @staticmethod
    def run_command(command: list):
        """
        Run a system command safely and return the result.
        """
        try:
            if isinstance(command, str):
                command = shlex.split(command)  # Safely split string into list
                
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            # Log error or handle it
            print(f"Command failed: {e}")
            return None
