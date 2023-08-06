"""setup.py file."""
from setuptools import setup, find_packages

setup(
    name="tm_merger",
    version='0.0.3',
    packages=find_packages(exclude=("test*", "venv")),
    author="Federico Olivieri",
    author_email="federico.olivieri@ticketmaster.nl",
    description="Ansible module for base and tenant config merger.",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/lvrfrc87/tm_merger",
    install_requires='more_itertools',
)
