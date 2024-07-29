# setup.py
from setuptools import setup, find_packages
import os


def read_requirements(file_path):
    with open(file_path, "r") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

setup(
    name="thabit",
    version="0.2.2",
    packages=find_packages(),
    package_data={
        "thabit": ["templates/*"],
    },
    entry_points={
        "console_scripts": [
            "thabit=thabit.thabit:cli",
        ],
    },
    install_requires=read_requirements(requirements_path),
    description="Thabit: evaluate multiple LLMs on your data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oras Al-Kubaisi",
    author_email="code@oras.me",
    url="https://github.com/thabit-ai/thabit",
    classifiers=["Topic :: Utilities"],
    python_requires=">=3.6",
)
