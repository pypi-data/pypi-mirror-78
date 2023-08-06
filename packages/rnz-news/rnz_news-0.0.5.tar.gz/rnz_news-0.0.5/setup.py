import setuptools
import subprocess

# Retrive git version.
version = subprocess.run(
    ["git", "describe", "--tags", "--abbrev=0"],
    stdout=subprocess.PIPE).stdout.strip()[1:].decode('utf-8')

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rnz_news",
    version=version,
    author="Guangrui Wang",
    author_email="aguang.xyz@gmail.com",
    description="Retrieve RNZ news.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aguang-xyz/rnz-news",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>= 3.8',
)
