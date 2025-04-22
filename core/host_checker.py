# Host alive checking

from core.command_executor import CommandExecutor

class HostChecker:
    @staticmethod
    def check_host_alive(target: str):
        """
        Run `nmap -sn` to check if a host is alive (works for both individual IP and CIDR).
        """
        result = CommandExecutor.run_command(["nmap", "-sn", target])
        if result:
            live_ips = []
            for line in result.splitlines():
                if "Nmap scan report for" in line:
                    ip = line.split()[-1]
                    live_ips.append(ip)
            return live_ips
        return []
