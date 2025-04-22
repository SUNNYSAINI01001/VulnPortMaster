from core.scanner import Scanner
from utils.helpers import Helpers
from core.host_checker import HostChecker
from utils.logger import Logger

class CIDRScanner(Scanner):
    """
    Scanner for CIDR ranges.
    """

    def __init__(self, target, command):
        super().__init__(target, command)

    def scan(self):
        """
        Scan the CIDR range and check which hosts are alive.
        If the target is a single IP, skip the alive check since it's already known to be up.
        """
        # Step 1: Validate the target (either CIDR or individual IP)
        if not Helpers.validate_target(self.target):
            Logger.log_error(f"Invalid target: {self.target}")
            return []

        # Step 2: Check if the target is a CIDR range or an individual IP
        if Helpers.is_cidr(self.target):
            # If it's a CIDR range, scan for alive hosts in the range
            live_ips = HostChecker.check_host_alive(self.target)
            if live_ips:
                Logger.log_info(f"Found live hosts in CIDR range {self.target}: {', '.join(live_ips)}")
                # Step 3: Additional scanning or processing on the live hosts
                return live_ips
            else:
                Logger.log_error(f"No live hosts found for CIDR range: {self.target}")
                return []
        else:
            # If it's a single IP, we assume it's already up and running, no need to check
            Logger.log_info(f"Target IP {self.target} is already up.")
            # Proceed with further scanning
            return [self.target]
