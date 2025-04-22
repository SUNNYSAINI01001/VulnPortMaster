# Main Entry Point

import sys
from core.cidr_scanner import CIDRScanner
from core.ip_scanner import IPScanner
from utils.logger import Logger

def main():
    # Step 1: Accept target from the user
    if len(sys.argv) < 2:
        Logger.log_error("No target specified. Please provide an IP address or CIDR range.")
        return

    target = sys.argv[1]  # Target IP or CIDR range

    # Step 2: Determine the scan type based on the target
    if '/' in target:  # CIDR range
        Logger.log_info(f"Target is a CIDR range: {target}")
        cidr_scanner = CIDRScanner(target, None)
        live_ips = cidr_scanner.scan()

        if live_ips:
            Logger.log_info("Starting scans on live hosts...")
            ip_scanner = IPScanner(live_ips, None)
            ip_scanner.scan()
        else:
            Logger.log_error("No live IPs found. Skipping further scanning.")

    else:  # Single IP
        Logger.log_info(f"Target is a single IP: {target}")
        ip_scanner = IPScanner(target, None)
        ip_scanner.scan()

if __name__ == "__main__":
    main()
