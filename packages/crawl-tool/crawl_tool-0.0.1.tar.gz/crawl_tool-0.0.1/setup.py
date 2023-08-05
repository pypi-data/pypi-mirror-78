# -*- coding: utf-8 -*-
# @Time    : 2020/8/31 18:19
# @Author  : meng_zhihao
# @Email   : 312141830@qq.com
# @File    : setup.py
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawl_tool", # Replace with your own username
    version="0.0.1",
    author="zhihao.meng",
    author_email="meng631011@gmail.com",
    description="Tool class for web crawling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MemoryAndDream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)