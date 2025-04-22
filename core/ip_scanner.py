from core.scanner import Scanner
from utils.logger import Logger
from core.command_executor import CommandExecutor
import re

class IPScanner(Scanner):
    """
    Scanner for individual IP addresses or a list of IPs with multiple commands.
    """

    def __init__(self, target, commands=None):
        if commands is None:
            commands = [
                "nmap -F -sV {ip}",  # Default scan
                "nmap -vvv -p- {ip} --open -T4 -Pn --max-retries 1 --max-scan-delay 20 --defeat-rst-ratelimit",  # Full Port Scan
                "nmap -sV -vvv -p{ports} -A {ip} --script vuln --max-retries 1 --max-scan-delay 20 -T4 -Pn --stats-every 3m -oN full_nmap.txt",  # In-Depth Scan
            ]
        super().__init__(target, commands)

    def scan(self):
        targets = [self.target] if isinstance(self.target, str) else list(set(self.target))  # remove duplicates

        scanned = set()

        for ip in targets:
            if ip in scanned:
                continue
            scanned.add(ip)

            self._run_command(self.command[0], ip)

            full_port_scan_result = self._run_command(self.command[1], ip)

            if full_port_scan_result:
                open_ports = self._extract_open_ports(full_port_scan_result)
                if open_ports:
                    open_ports_str = ','.join(map(str, open_ports))
                    Logger.log_info(f"Found open ports: {open_ports_str}")

                    in_depth_command = self.command[2].replace("{ports}", open_ports_str)
                    self._run_command(in_depth_command, ip)
                else:
                    Logger.log_error(f"No open ports found for {ip}. Skipping in-depth scan.")
            else:
                Logger.log_error(f"Full port scan failed for {ip}. Skipping in-depth scan.")


    # def scan(self):
    #     # Normalize to a list (whether it's a single IP or list of IPs)
    #     targets = [self.target] if isinstance(self.target, str) else self.target

    #     for ip in targets:
    #         # First, perform the default scan (or any scan you need to kick off)
    #         self._run_command(self.command[0], ip)

    #         # Now, run the full port scan to find open ports
    #         full_port_scan_result = self._run_command(self.command[1], ip)

    #         # If open ports are found, extract them and prepare for the in-depth scan
    #         if full_port_scan_result:
    #             open_ports = self._extract_open_ports(full_port_scan_result)
    #             if open_ports:
    #                 open_ports_str = ','.join(map(str, open_ports))
    #                 Logger.log_info(f"Found open ports: {open_ports_str}")

    #                 # Run the in-depth scan using the open ports
    #                 in_depth_command = self.command[2].replace("{ports}", open_ports_str)
    #                 self._run_command(in_depth_command, ip)
    #             else:
    #                 Logger.log_error(f"No open ports found for {ip}. Skipping in-depth scan.")
    #         else:
    #             Logger.log_error(f"Full port scan failed for {ip}. Skipping in-depth scan.")

    def _run_command(self, command, ip):
        """
        Helper method to run a command using the CommandExecutor.
        """
        formatted_command = command.replace("{ip}", ip)
        Logger.log_info(f"Running command: {formatted_command}")

        result = CommandExecutor.run_command(formatted_command)

        if result:
            Logger.log_success(f"Scan result for {ip}:\n{result}")
            return result
        else:
            Logger.log_error(f"Scan failed or no result for {ip}")
            return None

    def _extract_open_ports(self, scan_result):
        """
        Extract open ports from the full port scan result.
        """
        # Regular expression to find open ports in the nmap output
        open_ports = []
        port_pattern = re.compile(r'(\d+)/tcp\s+open')
        matches = port_pattern.findall(scan_result)

        # If there are matches, return the list of open ports
        if matches:
            open_ports = [int(port) for port in matches]
        return open_ports
