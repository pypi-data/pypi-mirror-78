from setuptools import setup, find_packages

with open("requirements.in") as f:
    setup(
        name = "lonny_pg",
        version = "1.5",
        packages = find_packages(),
        install_requires = f.read().splitlines()
    )