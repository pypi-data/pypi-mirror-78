# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup, find_packages


# 将markdown格式转换为rst格式
# def md_to_rst(from_file, to_file):
#     try:
#         r = requests.post(url='http://c.docverter.com/convert',
#                           data={'to': 'rst', 'from': 'markdown'},
#                           files={'input_files[]': open(from_file, 'rb')})
#         if r.ok:
#             with open(to_file, "wb") as f:
#                 f.write(r.content)

#     except Exception as e:
#         print(str(e))


def set_long_description():
    long_description = ""
    if os.path.exists('README.md'):
        try:
            long_description = open('README.md', encoding="utf-8").read()
        except Exception as e:
            pass
    else:
        long_description = 'Add a fallback short description here'
    return long_description


def set_install_requires():
    install_requires = []
    if os.path.exists("requirements.txt"):
        install_requires = io.open("requirements.txt").read().split("\n")
    return install_requires


setup_attrs = {
    "name": 'pyeventbus2',  # zipfile name
    "version": '1.0.0',  # version
    "description": "Lightweight event bus support sync and async, inspired by google guava event bus",
    "keywords": 'eventbus',
    "author": 'shenxianjie',
    "author_email": '327411586@qq.com',
    "license": 'MIT',
    "url": "https://github.com/jxs1211/pyeventbus",
    "long_description": set_long_description(),
    "long_description_content_type": 'text/markdown',
    "classifiers": [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    "packages": find_packages(),
    "platforms": ["all"],
    # include_package_data: True,
    "zip_safe": True,
    "install_requires": set_install_requires()
}

if __name__ == "__main__":
    # md_to_rst("README.md", "README.rst")
    setup(**setup_attrs)
