from setuptools import setup, find_packages
import os

def post_install():
    # Install the systemd service file
    service_file = os.path.join(os.path.dirname(__file__), 'ltop.service')
    os.system(f'sudo cp {service_file} /etc/systemd/system/')
    os.system('sudo systemctl daemon-reload')
    os.system('sudo systemctl enable ltop.service')

# Function to read the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='ltop',
    version='0.1',
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'ltop-monitor=ltop.ltop:monitor_system',
            'ltop-log-retention=ltop.log_retention:delete_old_logs',
        ],
    },
    author='Priyanshu K',
    twitter="https://twitter.com/pkdevaa",
    author_email='priyanshu.txt@gmail.com',
    description='A versatile tool for SREs and DevOps to monitor system resources and log resource utilization.',
    url='https://github.com/pkdeva/ltop',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': post_install,
    }
)
