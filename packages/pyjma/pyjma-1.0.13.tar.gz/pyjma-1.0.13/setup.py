from setuptools import setup, find_packages
import codecs
import os
import re


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_install_requires():
    reqs = [
        'requests>=2.0.0',
        'xmltodict>=0.12.0'
    ]
    return reqs

setup(
    name='pyjma',
    version="1.0.13",
    description='A Python Library for Japan Disaster Data Extraction',
    # long_description=read("READM.rst"),
    # long_description=long_desc,
    author='Chenyi Liao',
    author_email='info@liaocy.net',
    license='MIT',
    url='https://github.com/liaocyintl/pyjma',
    install_requires=read_install_requires(),
    keywords='python disaster japan meteorological agency jma',
    classifiers=['Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
                 # Define that your audience are developers
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'License :: OSI Approved :: MIT License',   # Again, pick a license
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)
