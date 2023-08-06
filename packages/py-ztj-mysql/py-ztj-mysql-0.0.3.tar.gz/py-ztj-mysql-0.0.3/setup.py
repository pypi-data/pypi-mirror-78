# -*- coding: utf-8 -*-
# Intro: mysql 实例模块安装文件
# Author: Ztj
# Email: ztj1993@gmail.com
# Date: 2019-09-04

import os.path
import re

from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8')
readme = f.read()
f.close()

f = open(os.path.join(os.path.dirname(__file__), 'ZtjMySQL.py'), encoding='utf8')
version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
f.close()

setup(
    name='py-ztj-mysql',
    version=version,
    description='python mysql instance package',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ZtjMySQL'],
    url='https://github.com/ztj-package/py-mysql',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='mysql',
    install_requires=[
        'pymysql',
        'DBUtils',
        'py-ztj-registry>=0.0.4',
    ],
    license='MIT License',
)
