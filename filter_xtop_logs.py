import re
from datetime import datetime

LOG_FILE = '/var/log/syslog'

def filter_logs(cpu_threshold=0, mem_threshold=0):
    pattern = re.compile(r'xtop: \[INFO\] Resource spike detected: CPU=(\d+\.?\d*)%, MEM=(\d+\.?\d*)%')
    process_pattern = re.compile(r'xtop: \[INFO\] Process info: PID=(\d+), Name=(\S+), CPU%=(\d+\.?\d*), MEM%=(\d+\.?\d*), Directory=(\S+)')
    
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    for line in lines:
        match = pattern.search(line)
        if match:
            cpu_percent = float(match.group(1))
            mem_percent = float(match.group(2))
            if cpu_percent > cpu_threshold or mem_percent > mem_threshold:
                timestamp = line.split('xtop:')[0].strip()
                print(f'Timestamp: {timestamp}, CPU: {cpu_percent}%, Memory: {mem_percent}%')
                # Find the corresponding process details
                index = lines.index(line)
                while index + 1 < len(lines) and 'Process info:' in lines[index + 1]:
                    process_info = process_pattern.search(lines[index + 1])
                    if process_info:
                        pid = process_info.group(1)
                        name = process_info.group(2)
                        process_cpu = process_info.group(3)
                        process_mem = process_info.group(4)
                        directory = process_info.group(5)
                        print(f'    PID: {pid}, Name: {name}, CPU%: {process_cpu}, MEM%: {process_mem}, Directory: {directory}')
                    index += 1

if __name__ == "__main__":
    cpu_threshold = float(input("Enter CPU threshold (%): "))
    mem_threshold = float(input("Enter Memory threshold (%): "))
    filter_logs(cpu_threshold, mem_threshold)

