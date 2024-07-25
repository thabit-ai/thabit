# setup.py
from setuptools import setup, find_packages
import pathlib

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

base_dir = pathlib.Path(__file__).parent.resolve()
requirements_path = base_dir / 'requirements.txt'

setup(
    name="thabit",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'thabit=thabit.thabit:cli',
        ],
    },
    install_requires=read_requirements(requirements_path),
    description="Thabit: choose the right LLM for your data",
    author="Oras Al-Kubaisi",
    author_email="code@oras.me",
    url="https://github.com/thabit/thabit",
    classifiers=[
        "LLM",
        "Evaluation",
    ],
    python_requires='>=3.8',
)