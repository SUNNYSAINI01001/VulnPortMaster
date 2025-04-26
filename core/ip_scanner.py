from core.scanner import Scanner
from utils.logger import Logger
from core.command_executor import CommandExecutor
import re

class IPScanner(Scanner):
    """
    Scanner for individual IP addresses or a list of IPs with multiple commands.
    """

    def __init__(self, target, args):
        self.args = args

        commands = [
            "nmap -F -sV {ip}",  # Default scan
            "nmap -vvv -p- {ip} --open -T4 -Pn --max-retries 1 --max-scan-delay 20 --defeat-rst-ratelimit",  # Full Port Scan
            "nmap -sV -vvv -p{ports} -A {ip} --script vuln --max-retries 1 --max-scan-delay 20 -T4 -Pn --stats-every 3m -oN full_nmap.txt",  # In-Depth Scan
        ]

        super().__init__(target, commands)

    def scan(self):
        targets = [self.target] if isinstance(self.target, str) else list(set(self.target))  # Remove duplicates
        scanned = set()

        for ip in targets:
            if ip in scanned:
                continue
            scanned.add(ip)

            self._run_command(self.command[0], ip)

            # Separating output for readability
            print("#" * 50 + "\n" + "#" * 50 + "\n")
            full_port_scan_result = self._run_command(self.command[1], ip)
            print("#" * 50 + "\n" + "#" * 50 + "\n")
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

    def _run_command(self, command, ip):
        """
        Helper method to run a command using the CommandExecutor.
        """
        formatted_command = command.replace("{ip}", ip)

        # if self.args.dry_run:
        #     Logger.log_info(f"[DRY RUN] Would run: {formatted_command}")
        #     return None

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
        open_ports = []
        port_pattern = re.compile(r'(\d+)/tcp\s+open')
        matches = port_pattern.findall(scan_result)

        if matches:
            open_ports = [int(port) for port in matches]
        return open_ports
