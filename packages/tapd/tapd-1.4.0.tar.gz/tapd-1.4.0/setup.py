# coding:utf-8

"""
Author ：daben_chen
发布pypi tapd version = "1.0.0"
"""

from setuptools import setup, find_packages


setup(
    name = "tapd",
    license='Apache License 2.0',
    author = "chendb",
    author_email = "love_vida@163.com",
    description = "TAPD service driver",
    version = "1.4.0",
    url = "https://gitlab.pin-dao.cn/TM-QA",
    packages=find_packages(),
    platforms="any",
    install_requires = [
        "requests>=2.2.1",
    ]
)