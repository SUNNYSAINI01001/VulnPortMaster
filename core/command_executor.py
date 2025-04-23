# Executes specified commands

import subprocess
import shlex
from utils.logger import Logger

class CommandExecutor:
    @staticmethod
    def run_command(command: list):
        """
        Run a system command safely and return the result or classified error.
        """
        try:
            if isinstance(command, str):
                command = shlex.split(command)  # Safely split string into list

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

            return result.stdout

        except subprocess.CalledProcessError as e:
            stdout = e.stdout.lower()
            stderr = e.stderr.lower()

            error_type = CommandExecutor.classify_error(stdout + stderr)

            Logger.log_error(f"Command failed ({error_type}): {e}")
            return None

        except FileNotFoundError:
            Logger.log_error("Command not found. Is Nmap installed?")
            return None

        except Exception as e:
            Logger.log_error(f"Unexpected error while executing command: {str(e)}")
            return None

    @staticmethod
    def classify_error(output: str) -> str:
        """
        Classify the type of error based on output.
        """

        if "network is unreachable" in output:
            return "Network Unreachable"

        if "host seems down" in output or "0 hosts up" in output:
            return "Host Down"

        if "connection refused" in output:
            return "Port Blocked"

        if "timed out" in output or "retrying" in output:
            return "Timeout"

        if "command not found" in output or "nmap: not found" in output:
            return "Command Not Found"

        return "Unknown Error"
