from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


setup(
    name='gong_test_pub',
    version='1.0.5',
    description=(
        '<项目的简单描述>'
    ),
    long_description=open('README.md').read(),
    author='gong',
    author_email='2976560783@qq.com',
    maintainer='gong',
    maintainer_email='2976560783@qq.com',
    license='Apache License',
    packages=find_packages(),
    url='https://gitee.com/gongzhengyang',
    platforms=["all"],
    classifiers=[
    ],
)