
from setuptools import setup

setup(

    name='motoko',
    version='1.0.0',
    description='Smart servers management tools',
    long_description='Management tools and services for smart servers platform.',
    author='Luiz Viana',
    author_email='lviana@include.io',
    maintainer='Luiz Viana',
    maintainer_email='lviana@include.io',
    url='https://github.com/lviana/motoko',
    packages=['motoko'],
    package_dir={'motoko': 'src/lib'},
    licence='Apache',

    data_files=[
                    ('/usr/bin', ['src/bin/motoko']),
                    ('/etc/motoko', ['src/etc/motoko.conf']),
                    ('/etc/motoko', ['src/etc/server.tmpl']),
                    ('/etc/motoko', ['src/etc/client.tmpl'])
                ]

)
