import setuptools

with open ("README.md","r") as fh:
        long_description=fh.read()
setuptools.setup(
    name="mxmulaac_pkg",  #pypi中的名称，pip或者easy_install安装时使用的名称
    version="1.0",
    author="bigskeleton",
    author_email="bigskeleton@gmail.com",
    description=("An example for teaching how to publish a Python package"),
    # url="https://ssl.xxx.org/redmine/projects/RedisRun",
    packages=setuptools.find_packages(),       # 需要打包的目录列表

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
    
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ]
        )
