
from setuptools import setup

setup(

    name='mtktool',
    version='1.0.0',
    description='Smart servers management CLI',
    long_description='Management command line interface for motoko.',
    author='Luiz Viana',
    author_email='lviana@include.io',
    maintainer='Luiz Viana',
    maintainer_email='lviana@include.io',
    url='https://github.com/lviana/motoko',
    licence='Apache',

    data_files=[
                    ('/usr/bin', ['src/bin/mtktool']),
                    ('/etc/motoko', ['src/etc/mtktool.conf'])
                ]

)
