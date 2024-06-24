from setuptools import setup, find_packages

setup(
    name='ltop',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psutil',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'ltop-monitor=ltop.ltop:monitor_system',
            'ltop-log-retention=ltop.log_retention:delete_old_logs',
        ],
    },
    author='Priyanshu K',
    author_email='priyanshu.txt@gmail.com',
    description='A versatile tool for SREs and DevOps to monitor and log system resource utilization.',
    url='https://github.com/pkdeva/ltop',
    classifiers=[
        'Programming Language :: Python :: 3',1
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
