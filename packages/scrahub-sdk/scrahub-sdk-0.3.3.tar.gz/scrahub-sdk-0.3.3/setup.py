from setuptools import setup, find_packages

import scrahub.config

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='scrahub-sdk',
    version=scrahub.config.VERSION,
    packages=find_packages(),
    url='https://github.com/zwgk/scrahub-sdk',
    license='BSD-3-Clause',
    author='lsyer',
    author_email='lishao378@sohu.com',
    description='Python SDK for Scrahub',
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'Click==7.0',
        'requests==2.22.0',
        'prettytable==0.7.2',
        'scrapy==2.2.0',
        'pymongo==3.10.1',
        'pymysql==0.9.3',
        'psycopg2-binary==2.8.5',
        'kafka-python==2.0.1',
        'elasticsearch==7.8.0',
	'pathspec==0.8.0',
    ],
    entry_points={
        'console_scripts': [
            'scrahub=scrahub:main'
        ]
    }
)
