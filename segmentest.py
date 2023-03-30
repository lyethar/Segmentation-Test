import os
import subprocess
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--scope", type=str,
                        help="The scope.txt file.")

    return parser.parse_args()


def tcp(scope):
    output_file = "tcp_hosts.txt"
    scope_file = scope
    if os.path.exists(output_file):
        os.remove(output_file)
    if not os.path.exists(scope_file):
        print("Error: scope.txt file not found.")
        exit(1)

    with open(scope_file, "r") as file:
        subnets = [line.strip() for line in file if line.strip()]

    # Perform the Nmap scan on each subnet
    for subnet in subnets:
        print(f"Scanning subnet {subnet}...")
        print("nmap -Pn -sS --open {subnet}")
        result = subprocess.check_output(["nmap", "-Pn", "-sS", "--open", "-oA", "tcp_out", subnet], text=True)
        print(result)
        # Check if any open ports were found
        if "open" in result:
            print(f"Open ports found in subnet {subnet}:")
            ips_with_open_ports = [line.split()[4] for line in result.splitlines() if "Nmap scan report for" in line]
            with open(output_file, "a") as file:
                for ip in ips_with_open_ports:
                    print(f"IP: {ip}")
                    file.write(ip + "\n")
                    print(f"Saved to {output_file}")
        else:
            print(f"No open ports found in subnet {subnet}")

def icmp(scope):
    output_file = "icmp_hosts.txt"
    scope_file = scope
    if os.path.exists(output_file):
        os.remove(output_file)
    if not os.path.exists(scope_file):
        print("Error: scope.txt file not found.")
        exit(1)

    with open(scope_file, "r") as file:
        subnets = [line.strip() for line in file if line.strip()]

    # Perform the Nmap scan on each subnet
    for subnet in subnets:
        print(f"Scanning subnet {subnet}...")
        print("nmap -sn {subnet}")
        result = subprocess.check_output(["nmap", "-sn", "-oA", "icmp_out", subnet], text=True)
        print(result)
        # Check if any open ports were found
        if "Nmap scan report for" in result:
            print(f"Open ports found in subnet {subnet}:")
            ips_with_open_ports = [line.split()[4] for line in result.splitlines() if "Nmap scan report for" in line]
            with open(output_file, "a") as file:
                for ip in ips_with_open_ports:
                    print(f"IP: {ip}")
                    file.write(ip + "\n")
                    print(f"Saved to {output_file}")
        else:
            print(f"No hosts identified using ICMP {subnet}")
def udp(scope):
    output_file = "udp_hosts.txt"
    scope_file = scope
    if os.path.exists(output_file):
        os.remove(output_file)
    if not os.path.exists(scope_file):
        print("Error: scope.txt file not found.")
        exit(1)

    with open(scope_file, "r") as file:
        subnets = [line.strip() for line in file if line.strip()]

    # Perform the Nmap scan on each subnet
    for subnet in subnets:
        print(f"Scanning subnet {subnet}...")
        print("nmap -Pn -sU --max-retries 3 --open {subnet}")
        result = subprocess.check_output(["nmap", "-Pn", "-sU", "--open", "--max-retries", 3 , "-oA", "tcp_out", subnet], text=True)
        print(result)
        # Check if any open ports were found
        if "open" in result:
            print(f"Open ports found in subnet {subnet}:")
            ips_with_open_ports = [line.split()[4] for line in result.splitlines() if "Nmap scan report for" in line]
            with open(output_file, "a") as file:
                for ip in ips_with_open_ports:
                    print(f"IP: {ip}")
                    file.write(ip + "\n")
                    print(f"Saved to {output_file}")
        else:
            print(f"No open ports found in subnet {subnet}")
    
   
def main():
    args = parse_args()
    scope = args.scope
    icmp(scope)
    tcp(scope)
    udp(scope)
   
  
if __name__ == '__main__':
    main()
