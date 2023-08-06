import re
import sys
from os import path as op

from setuptools import setup


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname)).read()
    except IOError:
        return ''


def get_dependencies(dependency_file):
    return [
        line for line in _read(dependency_file).split('\n')
        if line and not line.startswith('#')
    ]


install_requires = get_dependencies('requirements.txt')

tests_require = get_dependencies('requirements-tests.txt')

setup(
    name='allokation',
    packages=['allokation'],
    version='0.0.1',
    python_requires='>=3.8',
    license='MIT License',
    description="""
    A python package that gets stocks prices from yahoo finance (https://finance.yahoo.com/)
    and calculates how much of each stocks you must buy to have almost equal distribution
    between the stocks you want in your portfolio
    """,
    long_description=_read('README.md'),
    long_description_content_type='text/markdown',
    author='Rafael Capaci',
    author_email='rafaelcapacipereira@gmail.com',
    url='https://github.com/capaci/allokation',
    download_url='https://github.com/capaci/allokation/archive/0.0.1.tar.gz',
    keywords=['finance', 'stocks', 'portfolio allocation'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Other Audience',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests',

)
