import argparse
from core.cidr_scanner import CIDRScanner
from core.ip_scanner import IPScanner
from utils.logger import Logger

def main():
    # Define argument parser
    parser = argparse.ArgumentParser(description="VulnPortMaster - Scan a CIDR range or a single IP using Nmap")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cidr', help='CIDR range to scan (e.g., 192.168.1.0/24)')
    group.add_argument('--ip', help='Single IP address to scan (e.g., 192.168.1.1)')

    # parser.add_argument('--dry-run', action='store_true', help='Show what would be run without executing')
    # parser.add_argument('--json', action='store_true', help='Export output in JSON format (feature placeholder)')
    # parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # if args.verbose:
    #     Logger.log_info("Verbose mode is enabled.")

    # if args.dry_run:
    #     Logger.log_info("Dry-run mode is enabled. No scans will be performed.")

    if args.cidr:
        Logger.log_info(f"Target is a CIDR range: {args.cidr}")
        # if args.dry_run:
        #     Logger.log_info(f"Would scan CIDR range: {args.cidr}")
        #     return
        cidr_scanner = CIDRScanner(args.cidr, args)
        live_ips = cidr_scanner.scan()

        if live_ips:
            Logger.log_info("Starting scans on live hosts...")
            ip_scanner = IPScanner(live_ips, args)
            ip_scanner.scan()
        else:
            Logger.log_error("No live IPs found. Skipping further scanning.")

    elif args.ip:
        Logger.log_info(f"Target is a single IP: {args.ip}")
        # if args.dry_run:
        #     Logger.log_info(f"Would scan IP: {args.ip}")
        #     return
        ip_scanner = IPScanner(args.ip, args)
        ip_scanner.scan()

if __name__ == "__main__":
    main()
