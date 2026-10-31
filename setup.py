from setuptools import setup, find_packages

setup(
    name="dynamic-test-subset-routing",
    version="1.0.0",
    description="Enterprise-grade Change-Based Predictive Test Impact Analysis and Sharding Engine for CI/CD",
    author="Saksham Singh",
    author_email="sakshamsingh819@gmail.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.7",
        "networkx>=3.2.1",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dtsr=src.dtsr.cli:main",
        ],
    },
)
