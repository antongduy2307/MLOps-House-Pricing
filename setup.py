from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="house-pricing",
    version="0.1",
    author="Tong Duy An",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
)