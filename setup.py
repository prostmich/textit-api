import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="textit-api",
    version="0.0.1",
    author="Mikhail Smolnikov",
    author_email="smolnik.mikhail@gmail.com",
    description="Useful tools for working with Russian text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prostmich/textit-api",
    project_urls={"Bug Tracker": "https://github.com/prostmich/textit-api/issues"},
    license="MIT",
    packages=find_packages(),
    install_requires=["aiohttp>=3.7.2,<4.0.0"],
)
