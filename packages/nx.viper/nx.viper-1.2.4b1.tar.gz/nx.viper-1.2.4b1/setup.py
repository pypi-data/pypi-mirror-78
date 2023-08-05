"""nx.viper"""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nx.viper',
    version='1.2.4b1',

    description='Application development framework for twisted.',
    long_description=long_description,

    url='https://github.com/Nixiware/viper',

    author='Nixiware',
    author_email='contact@nixiware.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='nixiware viper twisted',

    packages=[
        'nx.viper',
        'nx.viper.service'
    ],

    install_requires=['twisted', 'autobahn', 'PyMySQL'],
)