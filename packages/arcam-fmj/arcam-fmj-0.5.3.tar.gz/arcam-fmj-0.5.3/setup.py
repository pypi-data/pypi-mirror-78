from setuptools import find_packages, setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="arcam-fmj",
    version="0.5.3",
    description="A python library for speaking to Arcam receivers",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    packages=["arcam.fmj"],
    package_dir={"": "src"},
    python_requires=">=3.7",
    author="Joakim Plate",
    install_requires=["attrs>18.1", "aionursery"],
    extras_require={
        "tests": [
            "pytest>3.6.4",
            "pytest-aiohttp",
            "pytest-cov<2.6",
            "coveralls",
            "pytest-mock",
            "asynctest",
            "aiohttp",
            "defusedxml"
        ]
    },
    entry_points={"console_scripts": ["arcam-fmj=arcam.fmj.console:main"]},
    url="https://github.com/elupus/arcam_fmj",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Framework :: AsyncIO",
    ],
)
