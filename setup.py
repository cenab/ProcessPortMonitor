# setup.py

from setuptools import setup, find_packages

setup(
    name='processportmonitor',
    version='0.1.4',
    author='Cenab Batu Bora',
    author_email='batu.bora.tech@gmail.com',
    description='Real-time monitoring of active TCP ports used by a specific process (PID)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cenab/processportmonitor',
    packages=find_packages(),
    install_requires=[
        'jc>=1.12',
    ],
    classifiers=[ 
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking',
    ],
    entry_points={
        'console_scripts': [
            'processportmonitor=processportmonitor.__main__:main',
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
)
