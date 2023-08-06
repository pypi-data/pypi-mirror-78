from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory,"README.md")) as f:
    long_description = f.read()
setup(
    name="instagramthiefBot",
    packages=find_packages(),
    description="The Thief of Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="duckcouncil",
    version="1.2",
    author_email="duckcouncil239@gmail.com",
    license="MIT",
    install_requires=["selenium","bs4","Pillow","psycopg2"]
)