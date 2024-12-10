import os
import platform
import subprocess
import socket
import re
import requests
from html_report import generate_html_report

# Function to check if an IP address is reachable using ping
def is_host_alive(ip):
    command = ["ping", "-c", "1", ip] if platform.system() != "Windows" else ["ping", "-n", "1", ip]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "ttl=" in result.stdout.lower():
            return True
        return False
    except subprocess.CalledProcessError:
        return False

# Network scan to find active devices
def scan_network(ip_range):
    alive_hosts = []
    print(f"Scanning IP range: {ip_range}.0/24")
    for i in range(1, 255):  # Iterate through all IP addresses in a Class C range
        ip = f"{ip_range}.{i}"
        if is_host_alive(ip):
            print(f"{ip} is alive")
            alive_hosts.append(ip)
        else:
            print(f"{ip} is not responding")
    return alive_hosts

# Function to scan open ports and identify services by port number
def scan_ports_and_services(ip):
    common_services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        8080: "HTTP Proxy",
        8443: "HTTPS Alt"
    }
    open_ports = []
    services = []
    for port in common_services.keys():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
                services.append(common_services[port])
                print(f"Port {port} on {ip} is open ({common_services[port]})")
            else:
                print(f"Port {port} on {ip} is closed")
    return open_ports, services

# Function to retrieve MAC address and identify hardware vendor
def get_mac_address_and_vendor(ip):
    try:
        result = subprocess.run(["arp", "-n", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        mac_address = re.search(r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})", result.stdout)
        if mac_address:
            mac = mac_address.group(0)
            vendor = get_vendor(mac)
            return mac, vendor
        else:
            return "MAC Address Not Found", "Unknown Vendor"
    except FileNotFoundError:
        return "ARP command not found", "Unknown Vendor"
    except Exception as e:
        return f"Error: {str(e)}", "Unknown Vendor"

# Function to identify hardware vendor by MAC address using the macvendors.co API
def get_vendor(mac_address):
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown Vendor"
    except Exception as e:
        return f"Error: {str(e)}"

# Network scan process
def main():
    network_range = input("Enter the network range (e.g., 192.168.1): ")
    active_ips = scan_network(network_range)

    scan_results = {}
    for ip in active_ips:
        print(f"Scanning ports and services for {ip}...")
        open_ports, services = scan_ports_and_services(ip)
        mac_address, vendor = get_mac_address_and_vendor(ip)

        scan_results[ip] = {
            "ip": ip,
            "open_ports": open_ports,
            "services": services,
            "mac_address": mac_address,
            "vendor": vendor
        }
        print(f"Open ports on {ip}: {open_ports}")
        print(f"Services on {ip}: {services}")
        print(f"MAC address for {ip}: {mac_address}")
        print(f"Vendor for {ip}: {vendor}")

    generate_html_report(scan_results)

if __name__ == "__main__":
    main()
