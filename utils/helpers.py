import ipaddress

class Helpers:
    @staticmethod
    def validate_target(target: str):
        """
        Validate if the target is a valid CIDR or IP address.
        """
        try:
            ipaddress.ip_network(target)  # Validates CIDR range
            return True
        except ValueError:
            try:
                ipaddress.ip_address(target)  # Validates single IP address
                return True
            except ValueError:
                return False

    @staticmethod
    def is_cidr(target: str) -> bool:
        """
        Check if the target is a CIDR range.
        """
        try:
            ipaddress.ip_network(target)  # If this doesn't raise an exception, it's a CIDR range
            return True
        except ValueError:
            return False
