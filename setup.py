import os
import subprocess
from setuptools import setup, find_packages

# Create a virtual environment
venv_path = '/opt/ltop/venv'
if not os.path.exists(venv_path):
    subprocess.check_call(['python3', '-m', 'venv', venv_path])

# Install dependencies in the virtual environment
subprocess.check_call([f'{venv_path}/bin/pip', 'install', '-r', 'requirements.txt'])

# Write the systemd service file
service_content = """[Unit]
Description=Ltop System Resource Monitor
After=network.target

[Service]
ExecStart=/opt/ltop/venv/bin/python3 -m ltop.ltop
Restart=always
User=root

[Install]
WantedBy=multi-user.target
"""

service_path = '/etc/systemd/system/ltop.service'
with open(service_path, 'w') as service_file:
    service_file.write(service_content)

# Reload systemd daemon and enable the service
subprocess.check_call(['systemctl', 'daemon-reload'])
subprocess.check_call(['systemctl', 'enable', 'ltop.service'])
subprocess.check_call(['systemctl', 'restart', 'ltop.service'])

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='ltop',
    version='1.0',
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ltop=ltop.ltop:main',
        ],
    },
)
