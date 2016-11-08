#!/usr/bin/env python3

from setuptools import setup, find_packages
from pathlib import Path

desc = Path(__file__).parent.resolve().joinpath('README.md')
with desc.open(encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='d',
    version='0.1',
    description='A simple CLI task management tool',
    long_description=long_description,
    url='https://github.com/vitaliy.pisnya/do.git',
    author='Vitaliy Pisnya',
    author_email='vitaliy.pisnya@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='tasks management',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'd=d:main',
        ],
    },
)
