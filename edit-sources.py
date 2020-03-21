from os import system, getuid
import sys
import subprocess
import pathlib
import ipaddress
import argparse


SOURCES_FILE = "sources.list"
SOURCES_PATH = pathlib.Path("/etc/apt/")
SOURCES_BACKUP_FILE = "sources.bak"


def validate_ip(addr: str) -> str:
    if ipaddress.ip_address(addr):
        return addr
    else:
        raise argparse.ArgumentError()


def validate_port(port: str) -> str:
    if port.isdigit() and (1 <= int(port) <= 65535):
        return port
    else:
        raise argparse.ArgumentError()


def check_for_backup():
    if pathlib.Path.exists(SOURCES_PATH / SOURCES_BACKUP_FILE):
        print(f"Found existing backup:\t{SOURCES_PATH / SOURCES_BACKUP_FILE}")
        return True
    else:
        print("No existing backup found")
        return False


def restore_backup():
    try:
        system(f"cp {SOURCES_PATH / SOURCES_BACKUP_FILE} {SOURCES_PATH / SOURCES_FILE}")
        print(f"Restored sources using backup:\t{SOURCES_PATH / SOURCES_BACKUP_FILE}")
        system(f"rm {SOURCES_PATH / SOURCES_BACKUP_FILE}")
        print("Removed old backup")
    except Exception as e:
        print(e)


def backup_sources():
    if pathlib.Path.exists(SOURCES_PATH / SOURCES_FILE):
        print(f"Found sources:\t{SOURCES_PATH / SOURCES_FILE}")

    try:
        system(f"cp {SOURCES_PATH / SOURCES_FILE} {SOURCES_PATH / SOURCES_BACKUP_FILE}")
        print(f"Existing sources backed up to:\t {SOURCES_PATH / SOURCES_BACKUP_FILE}")
    except Exception as e:
        print(e)


def make_line_change(old_line):
    temp = old_line.split("//")
    return temp[0] + "//" + args.ip_addr + ":" + args.port + "/" + temp[1]


def read_modify_save():
    temp = ""
    try:
        with open(SOURCES_PATH / SOURCES_FILE, "r") as f:
            for line in f.readlines():
                if line.startswith("deb"):
                    temp += make_line_change(line)
                else:
                    temp += line

        with open(SOURCES_PATH / SOURCES_FILE, "w") as f:
            f.write(temp)

        print(f"Changes successfully written to:\t{SOURCES_PATH / SOURCES_FILE}")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    # Check for root. If not, ask for root.
    if getuid() == 0:
        print("Running as root...")
    else:
        print("Root is required to modify /etc/apt/sources.list")
        subprocess.call(['sudo', 'python3', *sys.argv])
        sys.exit()

    parser = argparse.ArgumentParser(description="Backs up existing apt sources.list and inserts desired IP address.",
                                     allow_abbrev=True, epilog="Brought to you by Dingus Enterprises")
    parser.add_argument("-i", "--ip-addr", help="IP of the apt-cacher-ng instance", type=validate_ip, action="store")
    parser.add_argument("-p", "--port", help="Port of the apt-cacher-ng instance", type=validate_port, action="store")
    parser.add_argument("-r", "--restore", help="Restore sources from backup", action="store_true")

    args = parser.parse_args()

    if args.restore:
        if check_for_backup():
            restore_backup()
            exit(0)
        else:
            exit(0)

    if args.ip_addr and args.port:
        if check_for_backup():
            restore_backup()
            backup_sources()
            read_modify_save()
        else:
            backup_sources()
            read_modify_save()

    else:
        print("IP and/or port required")
        exit(1)
