from __future__ import print_function
from setuptools import setup, find_packages
import send_to_log_center_ys

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="send-log-ys",
    version=send_to_log_center_ys.__version__,
    author="wiken",
    author_email="wiken01@qq.com",
    description="send log to log_center for ys",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/wikensmith/send_to_log_center_ys.git",  # git 地址
    packages=find_packages(),
    install_requires=[
        "requests==2.24.0",
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
