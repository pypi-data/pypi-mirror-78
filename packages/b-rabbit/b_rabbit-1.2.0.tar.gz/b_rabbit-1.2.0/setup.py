#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['rabbitpy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Nidhal Baccouri",
    author_email='nidhalbacc@gmail.com',
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="An abstract interface for RabbitMQ communication",
    install_requires=requirements,
    #long_description_content_type='text/markdown',
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='b_rabbit',
    name='b_rabbit',
    packages=find_packages(include=['b_rabbit', 'b_rabbit.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nidhaloff/b_rabbit',
    version='1.2.0',
    zip_safe=False,
)
