import sys

from setuptools import setup, find_packages

if sys.version_info[: 2] < (3, 6):
    raise RuntimeError('Python version >= 3.6 required')

MAJOR = 0
MINOR = 9
MICRO = 14
VERSION = f'{MAJOR}.{MINOR}.{MICRO}'

PACKAGES = ['tcontrol'] + [f"tcontrol.{i}" for i in find_packages('tcontrol')]

long_description = open('./README.md', encoding="utf-8").read()

setup(
    name='TControl',
    version=VERSION,
    author='HOUXIN LUO',
    author_email='2577229471@qq.com',
    packages=PACKAGES,
    license='BSD 3-clause',
    install_requires=['sympy>=1.0', 'numpy>=1.12.0', 'matplotlib>=2.0.0', 'scipy>=1.1.0'],
    tests_requires=['nose2>=0.7.4'],
    extra_requires={
        'doc': ['sphinx>=1.6.6', 'sphinx-rtd-theme>=0.4.0']
    },
    description="用于自动控制系统分析的Python库。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ljcloud/TControl",
)
