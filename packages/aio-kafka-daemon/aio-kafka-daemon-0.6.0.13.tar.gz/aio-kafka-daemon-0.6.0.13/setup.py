#!/usr/bin/env python3
"""aio-kafka-daemon setup"""

from distutils.core import setup

from setuptools import find_packages

setup(
    name="aio-kafka-daemon",
    version="0.6.0.13",
    description="Asynchronous Kafka Processing Daemon",
    author="Bob Zhou",
    author_email="bob.zhou@ef.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="asyncio-based kafka producer/consumer daemon framework",
    url="",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "venv"]),
    install_requires=["asyncio", "aiokafka==0.6.0", "boto3", "crc32c", "python-snappy"],
    tests_require=["pytest", "pytest-asyncio", "pytest-cov", "pytest-mock", "coverage"],
    python_requires=">=3.7, <4",
    entry_points={"console_scripts": []},
)
