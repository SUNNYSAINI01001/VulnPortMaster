from core.scanner import Scanner
from utils.helpers import Helpers
from core.host_checker import HostChecker
from utils.logger import Logger

class CIDRScanner(Scanner):
    """
    Scanner for CIDR ranges.
    """

    def __init__(self, target, args):
        super().__init__(target, args)
        self.args = args  # store parsed CLI arguments if needed

    def scan(self):
        """
        Scan the CIDR range and check which hosts are alive.
        """
        if not Helpers.validate_target(self.target):
            Logger.log_error(f"Invalid target: {self.target}")
            return []

        if Helpers.is_cidr(self.target):
            # if self.args.dry_run:
            #     Logger.log_info(f"[DRY RUN] Would scan CIDR range: {self.target}")
            #     return []

            live_ips = HostChecker.check_host_alive(self.target)
            if live_ips:
                Logger.log_info(f"Found live hosts in CIDR range {self.target}: {', '.join(live_ips)}")
                return live_ips
            else:
                Logger.log_error(f"No live hosts found for CIDR range: {self.target}")
                return []
        else:
            Logger.log_info(f"Target IP {self.target} is already up.")
            return [self.target]
