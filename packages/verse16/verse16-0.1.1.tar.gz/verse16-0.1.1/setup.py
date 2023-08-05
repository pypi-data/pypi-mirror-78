#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "tensorflow-gpu<=1.15.3",
    "progressbar2",
    "pronouncing",
    "syllables",
    "gpt-2-simple",
    "progressist"
]

setup_requirements = []

test_requirements = []

setup(
    author="pelgo14",
    author_email='pelgo14@protonmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="nlp rap text-generation",
    entry_points={
        'console_scripts': [
            'verse16=verse16.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='verse16 nlp rap text-generation',
    name='verse16',
    packages=find_packages(include=['verse16', 'verse16.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pelgo14/verse16',
    version='0.1.1',
    zip_safe=False,
)
