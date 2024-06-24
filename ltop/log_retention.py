import os
import time

LOG_DIR = '/var/log'
LOG_FILE_PREFIX = 'ltop.log'
RETENTION_PERIOD = 24 * 3600  # 24 hours in seconds

def delete_old_logs():
    now = time.time()
    for filename in os.listdir(LOG_DIR):
        if filename.startswith(LOG_FILE_PREFIX) and filename.endswith('.log'):
            file_path = os.path.join(LOG_DIR, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                if now - file_stat.st_mtime > RETENTION_PERIOD:
                    try:
                        os.remove(file_path)
                        print(f"Deleted old log file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    delete_old_logs()


# To automate the execution of log_retention.py script, we would need to set up a cron job that runs daily to delete old log files.
# something like:            0 0 * * * /usr/bin/python3 /path/to/log_retention.py


