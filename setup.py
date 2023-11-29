from setuptools import setup, find_packages

setup(
    name="directorship",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "directorship = directorship.__main__:main",
        ]
    },
)
