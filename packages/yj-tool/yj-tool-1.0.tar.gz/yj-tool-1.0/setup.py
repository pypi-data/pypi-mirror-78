#!/usr/bin/env python

from setuptools import setup
import sys  # noqa

setup(
    name='yj-tool',
    version='1.0',
    description='A YAML to JSON convertor tool written in python.',
    author='Ankit Jain',
    license='Apache-2.0 License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords="yj, yaml-json, yaml convertor, yj-tool",
    author_email='ankitjain28may77@gmail.com',
    url='https://github.com/ankitjain28may/yj',
    packages=['yj'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'yj = yj.yj:main'
        ],
    }
)