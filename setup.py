from setuptools import setup, find_packages

setup(
    name='portmonitor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'jc',
    ],
    entry_points={
        'console_scripts': [
            'portmonitor=portmonitor.__main__:main',
        ],
    },
)
