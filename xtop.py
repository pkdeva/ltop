import psutil
import time
import logging
import os
from datetime import datetime

# Configure logging to a file
LOG_FILE = '/var/log/xtop.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s xtop: [%(levelname)s] %(message)s',
    datefmt='%b %d %H:%M:%S'
)

logger = logging.getLogger()

def log_top_processes():
    processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'exe']))
    top_processes = sorted(processes, key=lambda p: p.info['cpu_percent'], reverse=True)[:10]
    logger.info("Logging top 10 processes by CPU usage")
    for proc in top_processes:
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent', 'exe'])
            logger.info(f"Process info: PID={proc_info['pid']}, Name={proc_info['name']}, "
                        f"CPU%={proc_info['cpu_percent']}, MEM%={proc_info['memory_percent']}, "
                        f"Command={proc_info['exe']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            logger.error(f"Error retrieving process info: {e}")

def monitor_system():
    logger.info("Starting xtop system resource monitor")
    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)
            mem_percent = psutil.virtual_memory().percent
            logger.debug(f"CPU usage: {cpu_percent}%, Memory usage: {mem_percent}%")
            log_top_processes()  # Always log the top processes every 5 seconds
            time.sleep(5)
    except Exception as e:
        logger.error(f"Error in monitor_system: {e}")

if __name__ == "__main__":
    monitor_system()

