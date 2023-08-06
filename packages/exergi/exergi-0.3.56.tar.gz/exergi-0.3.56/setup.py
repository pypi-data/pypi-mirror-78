import pathlib
from setuptools import find_packages,setup

HERE = pathlib.Path(__file__).parent        # The directory containing this file
README = (HERE / "README.md").read_text()   # The text of the README file

links = []                                 
requires = []

# This call to setup() does all the work
setup(
    name="exergi",
    version="0.3.56",
    description="SE Libary for various tasks",
    long_description=README,
    long_description_content_type="text/markdown",
    author="KasperJanehag",
    author_email="kasper.janehag@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "pandas>=1.1.1",
        "boto3>=1.14.15",
        "tables",
        "numpy>=1.19.0",
        "psycopg2-binary",
        ],
)


