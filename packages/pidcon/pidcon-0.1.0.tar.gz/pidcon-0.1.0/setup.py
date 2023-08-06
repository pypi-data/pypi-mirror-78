from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["Events==0.3"]

setup(
    name="pidcon",
    version="0.1.0",
    author="Akram Abu Owaimer",
    author_email="Akram.AbuOwaimer@gmail.com",
    description="A package to handle simple PID controller",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/FutureTech-o/pidcon",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>3.3',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
