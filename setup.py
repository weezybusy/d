#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

p = Path().resolve().joinpath('README.md')
with p.open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='d',
    version='0.1',
    description='A simple CLI task management tool.',
    long_description=long_description,
    url='https://github.com/weezybusy/d',
    author='Vitaliy Pisnya',
    author_email='vitaliy.pisnya@gmail.com',
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='tasks management',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'd=d:main',
        ],
    },
)
