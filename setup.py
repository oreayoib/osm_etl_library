from setuptools import setup, find_packages

setup(
    name="osm_etl_library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",
        "matplotlib"
    ],
)