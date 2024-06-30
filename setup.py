from setuptools import setup, find_packages
import os
import subprocess
import sys

# Function to create a virtual environment and install dependencies
def setup_venv():
    venv_path = '/opt/ltop/venv'
    python_executable = sys.executable  # Use the current Python executable

    # Check if venv module is available; install if not
    try:
        subprocess.check_call([python_executable, '-m', 'venv', '--help'])
    except subprocess.CalledProcessError:
        install_venv()

    # Create virtual environment
    subprocess.check_call([python_executable, '-m', 'venv', venv_path])

    # Activate virtual environment and install dependencies
    activate_script = os.path.join(venv_path, 'bin', 'activate')
    subprocess.check_call(['bash', '-c', f'source {activate_script} && python -m ensurepip'])
    subprocess.check_call(['bash', '-c', f'source {activate_script} && pip install --upgrade pip'])
    subprocess.check_call(['bash', '-c', f'source {activate_script} && pip install -r requirements.txt'])

# Function to install python3-venv package if venv is not available
def install_venv():
    package_manager = None
    if os.path.exists('/usr/bin/apt'):
        package_manager = 'apt'
    elif os.path.exists('/usr/bin/yum'):
        package_manager = 'yum'
    elif os.path.exists('/usr/bin/dnf'):
        package_manager = 'dnf'
    else:
        raise RuntimeError("Unsupported package manager")

    try:
        subprocess.check_call([package_manager, 'install', 'python3-venv'])
    except subprocess.CalledProcessError:
        raise RuntimeError(f"Failed to install python3-venv using {package_manager}")

    # Retry creating the virtual environment
    subprocess.check_call([sys.executable, '-m', 'venv', '/opt/ltop/venv'])

# Function to copy the systemd service file to the correct location
def setup_service():
    service_src = 'ltop.service'
    service_dest = '/etc/systemd/system/ltop.service'
    subprocess.check_call(['cp', service_src, service_dest])
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
