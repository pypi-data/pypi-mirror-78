import io
import sys
from glob import glob

from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


about = {}
exec(read("src", "traingame", "__version__.py"), about)

requirements = read("requirements.txt").split()
requirements_dev = read("requirements_dev.txt").split()


setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url=about["__url__"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=requirements,
    extra_require={
        "dev": requirements_dev,
    },
    entry_points={
        "console_scripts": ["traingame=traingame.cli:app"],
    },
)
