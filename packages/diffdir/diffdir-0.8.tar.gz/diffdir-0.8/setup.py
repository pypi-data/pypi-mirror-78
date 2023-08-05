from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="diffdir",
    version="0.8",
    description="Diff directories",
    url="https://github.com/kjgfcdb/diffdir",
    license="MIT Licence",
    author="cdb",
    author_email="kjgfcdb@126.com",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms="any",
    install_requires=["colorama", "path"],
    scripts=[],
    entry_points={"console_scripts": ["diffdir = diffdir.main:main"]},
)
