#!/usr/bin/env python3
from setuptools import setup
import os
import io
import slacklog
import unittest


def read_text(path, default=""):
    """Read a UTF-8 text file safely."""
    if not os.path.exists(path):
        return default
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


# Collect long description from README/CHANGES (if present)
long_description = "\n\n".join(
    filter(None, [read_text("README.rst"), read_text("CHANGES.rst")])
)


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='*.py')
    return test_suite


setup(
    name='slacklog',
    version=slacklog.__version__,
    author='Mikko Värri',
    author_email='vmj@linuxbox.fi',
    maintainer='Ioannis Anagnostakis',
    maintainer_email='rizitis@gmail.com',
    project_urls={
        'Documentation': 'https://rizitis.github.io/slacklog/',
        'Source': 'https://github.com/rizitis/slacklog/tree/python3',
        'Build status': '',
    },
    url='https://github.com/rizitis/slacklog/tree/python3',
    description=slacklog.__doc__,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=['slacklog'],
    entry_points={
        'console_scripts': [
            'slacklog2atom      = slacklog.scripts:slacklog2atom',
            'slacklog2pyblosxom = slacklog.scripts:slacklog2pyblosxom',
            'slacklog2rss       = slacklog.scripts:slacklog2rss',
            'slacklog2txt       = slacklog.scripts:slacklog2txt',
            'slacklog2json      = slacklog.scripts:slacklog2json',
        ]
    },
    python_requires='>=3.9,<4',
    install_requires=[
        'python-dateutil>=2.9,<3',
    ],
    extras_require={'docs': ['Sphinx>=2.9.0.20250822']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Topic :: Utilities',
    ],
    keywords='slackware changelog rss atom',
    test_suite='setup.my_test_suite',
)
