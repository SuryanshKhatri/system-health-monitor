
import json
import sys
from datetime import datetime
import argparse

# CLI argument setup
parser = argparse.ArgumentParser(description="System Health Monitor")
parser.add_argument("--raw", action="store_true", help="Use raw mode (no psutil)")
parser.add_argument("--cpu", action="store_true", help="Check CPU usage")
parser.add_argument("--mem", action="store_true", help="Check Memory usage")
parser.add_argument("--disk", action="store_true", help="Check Disk usage")
parser.add_argument("--all", action="store_true", help="Check all metrics (default)")
parser.add_argument("--log", default="log.txt", help="Path to log file")
args = parser.parse_args()

# Dynamic import
if args.raw:
    import utils_raw as sysmon
else:
    import psutil
    class sysmon:
        @staticmethod
        def get_cpu_usage():
            return psutil.cpu_percent(interval=1)
        @staticmethod
        def get_memory_usage():
            return psutil.virtual_memory().percent
        @staticmethod
        def get_disk_usage(path="/"):
            return psutil.disk_usage(path).percent

# Logging
def log_event(msg):
    with open(args.log, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def main():
    with open("config.json") as f:
        config = json.load(f)

    # Determine which metrics to check
    do_cpu = args.cpu or args.all or (not args.cpu and not args.mem and not args.disk)
    do_mem = args.mem or args.all or (not args.cpu and not args.mem and not args.disk)
    do_disk = args.disk or args.all or (not args.cpu and not args.mem and not args.disk)

    if do_cpu:
        cpu = sysmon.get_cpu_usage()
        log_event(f"CPU: {cpu}%")
        if cpu > config["cpu_threshold"]:
            log_event(f"⚠️ High CPU usage detected: {cpu}%")

    if do_mem:
        mem = sysmon.get_memory_usage()
        log_event(f"Memory: {mem}%")
        if mem > config["memory_threshold"]:
            log_event(f"⚠️ High Memory usage detected: {mem}%")

    if do_disk:
        disk = sysmon.get_disk_usage()
        log_event(f"Disk: {disk}%")
        if disk > config["disk_threshold"]:
            log_event(f"⚠️ High Disk usage detected: {disk}%")

if __name__ == "__main__":
    main()

