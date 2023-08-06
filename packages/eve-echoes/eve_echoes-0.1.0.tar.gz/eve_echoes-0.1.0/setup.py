from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="eve_echoes",
    summary="Eve Echoes Utility Functions",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Curtis Mason",
    author_email="cumason@bu.edu",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["eve_echoes.tests"]),
    version="0.1.0",
    install_requires=["numpy>1.19,<2.0"],
)
