import pathlib
from setuptools import setup

path = pathlib.Path(__file__).parent

README = (path / "README.md").read_text()

setup(
    name="jsearch",
    version="1.1.0",
    description="It implements all search algorithms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sjlouji/jsearch.git",
    author="Joan Louji",
    author_email="sjlouji10@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["jsearch"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "jsearch=src.__main__:main",
        ]
    },
)
