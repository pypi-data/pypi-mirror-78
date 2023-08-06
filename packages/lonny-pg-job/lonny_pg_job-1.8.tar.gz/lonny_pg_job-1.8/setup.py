from setuptools import setup, find_packages


with open("requirements.in") as f:
    setup(
        name = "lonny_pg_job",
        version = "1.8",
        packages = find_packages(),
        install_requires = f.read().splitlines()
    )