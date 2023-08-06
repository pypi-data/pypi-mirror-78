#!/usr/bin/env python
import io
from setuptools import setup, find_packages


readme = io.open('README.md', encoding='utf-8').read()


requirements = ['numpy', "sklearn", "sentencepiece"]

setup(
    # Metadata
    name='easydistill',
    version='0.0.1',
    python_requires='>=2.7',
    author='PAI NLP',
    author_email='haojie.phj@alibaba-inc.com',
    url='https://github.com/pypa/sampleproject',
    description='PAI EasyDistill Toolkit',
    long_description=readme,
    long_description_content_type='text/markdown',
    extras_require={
        "tf": ["tensorflow==1.12"],
        "tf_gpu": ["tensorflow-gpu==1.12"]
    },
    packages=find_packages(),
    license='Apache-2.0',

    # Package info
    install_requires=requirements
)
