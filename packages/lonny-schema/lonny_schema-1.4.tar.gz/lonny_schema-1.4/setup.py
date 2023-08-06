from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "lonny_schema",
        version = "1.4",
        packages = find_packages(),
        install_requires = f.read().splitlines()
    )