import re

import setuptools


def read_file(path):
    with open(path, "r") as handle:
        return handle.read()


def read_version():
    try:
        s = read_file("VERSION")
        m = re.match(r"v(\d+\.\d+\.\d+(-.*)?)", s)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


long_description = read_file("docs/source/description.rst")
version = read_version()

setuptools.setup(
    name="miniscule",
    description="""
    A YAML based, pluggable configuration library inspired by Aeson""",
    keywords="configuration",
    long_description=long_description,
    include_package_data=True,
    version=version,
    url="https://gitlab.com/bartfrenk/miniscule/",
    author="Bart Frenk",
    author_email="bart.frenk@gmail.com",
    package_dir={"miniscule": "src/miniscule"},
    entry_points={"console_scripts": ["miniscule = miniscule:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    # TODO: Make aws resolvers dependent on existence of boto3 dependency
    install_requires=["PyYAML>=3"],
    data_files=[(".", ["VERSION"])],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=4", "mock>=2.0.0", "boto3>=1.12.0,<2.0"],
    packages=setuptools.find_packages("src"),
)
