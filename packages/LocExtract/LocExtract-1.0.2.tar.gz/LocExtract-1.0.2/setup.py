#!/usr/bin/env python
#-*- coding:utf-8 -*-
from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "LocExtract",      #这里是pip项目发布的名称
    version = "1.0.2",  #版本号，数值大的会优先被pip
    keywords = ["pip", "LocExtract","LocationExtract"],
    description = "An china location extraction algorithm",
    long_description = "An china location extraction algorithm,",
    license = "MIT Licence",
    
    author = "lh",
    author_email = "huihuil@bupt.edu.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],          #这个项目需要的第三方库
)

