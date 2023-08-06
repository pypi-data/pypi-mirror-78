#!/usr/bin/env python

import io
import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
    long_description = readme.read()

name = 'allanc_sphinx'
description = 'Sphinx themes used for documentation of my projects.'

params = dict(
    name=name,
    use_scm_version=True,
    author="Allan Crooks",
    author_email="allan@sixtyten.org",
    description=description or name,
    long_description=long_description,
    license='MIT',
    url="https://github.com/the-allanc/" + name,
    packages=setuptools.find_packages(),
    include_package_data=True,
    setup_requires=[
        'setuptools_scm>=1.15.0'
    ],
    extras_require={
       'yeen': ['sphinxjp.themes.trstyle',]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Framework :: Sphinx :: Theme",
    ],
    entry_points={
        'sphinx.html_themes': [
            'path = allanc_sphinx:theme_path',
        ],
    },
)

if __name__ == '__main__':
    setuptools.setup(**params)
