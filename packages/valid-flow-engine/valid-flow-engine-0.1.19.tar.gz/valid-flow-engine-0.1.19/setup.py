import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="valid-flow-engine",
    version="0.1.19",
    description="Python Implementation of Valid Flow Engine",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jwaltgrant/py_valid_flow_engine",
    author="Josh Grant",
    author_email="jwaltgrant@gmail.com",
    license="GNU GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["python-dateutil"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
)
