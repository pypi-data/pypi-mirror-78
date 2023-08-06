#from distutils.core import setup
from setuptools import setup

with open("README.rst", "r",encoding='utf-8') as fh:
  long_description = fh.read()

setup(name="sztestliblib",#pip名
    version="1.0.1",
    description="this is a  ni lib",
    packages=["sztestlib"],# 包名
    py_modules=["Tool"],#单个文件
    author="sz",
    author_email="962296332@qq.com",
    long_description=long_description,
    url="https://github.com/pypa/sampleproject",
    license="MIT"
)