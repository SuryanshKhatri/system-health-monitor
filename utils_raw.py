
import os
import time

def get_cpu_usage():
    with open("/proc/stat", "r") as f:
        fields = list(map(int, f.readline().split()[1:]))
    idle1, total1 = fields[3], sum(fields)
    time.sleep(1)
    with open("/proc/stat", "r") as f:
        fields = list(map(int, f.readline().split()[1:]))
    idle2, total2 = fields[3], sum(fields)
    return round(100 * (1 - (idle2 - idle1) / (total2 - total1)), 2)

def get_memory_usage():
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, val = line.split(':')
            meminfo[key] = int(val.strip().split()[0])
    total = meminfo['MemTotal']
    available = meminfo['MemAvailable']
    return round(100 * (1 - available / total), 2)

def get_disk_usage(path="/"):
    stats = os.statvfs(path)
    total = stats.f_blocks * stats.f_frsize
    free = stats.f_bfree * stats.f_frsize
    used = total - free
    return round((used / total) * 100, 2)

