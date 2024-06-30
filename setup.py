from setuptools import setup, find_packages
import os
import subprocess
import sys

# Function to create a virtual environment and install dependencies
def setup_venv():
    venv_path = '/opt/ltop/venv'
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
    subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '--upgrade', 'pip'])
    subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])

# Function to set up the systemd service
def setup_service():
    service_content = """\
[Unit]
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
    subprocess.check_call(['systemctl', 'daemon-reload'])
    subprocess.check_call(['systemctl', 'enable', 'ltop'])
    subprocess.check_call(['systemctl', 'start', 'ltop'])

# Call the functions to set up the virtual environment and the service
setup_venv()
setup_service()

# Standard setup function
setup(
    name='ltop',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'ltop = ltop.ltop:main',
        ],
    },
)
