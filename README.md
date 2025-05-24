# VulnPortMaster

**VulnPortMaster** is an advanced Python-based tool designed for security professionals and ethical hackers to conduct vulnerability and port scanning on both individual targets and CIDR ranges. It leverages nmap for robust network scanning and vulnerability assessment, offering users a powerful solution for discovering open ports, services, and vulnerabilities in a given system.

The tool supports multiple scanning techniques, all built-in Python 3.13, for comprehensive network exploration. Whether you're scanning a single host or an entire subnet, VulnPortMaster makes it easy to automate and analyze security scans.

## Features

* **CIDR Range Scanning:** Efficiently scan an entire network range (CIDR) for live hosts, open ports & vulnerabilities.
* **Individual Target Scanning:** Scan specific IP addresses for open ports and vulnerabilities.
* **Nmap-Based Scanning:** Uses nmap for performing Three-Step Network Scanning techniques, including fast scan for initial discovery, all open port scan & In-Depth Vulnerability Scan using NSE.
* **Built-in Python 3.13:** Developed with Python 3.13, ensuring compatibility and efficiency.

## Setup

1. Clone the repository:
```
git clone https://github.com/d3athcod3/VulnPortMaster.git
```

2. Navigate to the directory:
```
cd VulnPortMaster
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. (Optional) Set up the virtual environment:
```
virtualenv VulnPortMaster_venv
source VulnPortMaster_venv/bin/activate
```

5. Run the tool with the desired target or CIDR range:
```
python portmaster.py <target_ip/CIDR_range>
```

## Requirements

Python 3.13 or higher
Nmap
Virtualenv (optional but recommended)

## License
This project is licensed under the BSD-3-Clause License.

## Contributing
Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.
