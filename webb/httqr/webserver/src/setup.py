from setuptools import setup
import os

# Do not install any packages here. State them in the
# requirements.txt file, and they will be suitably
# installed by the Dockerfile.

setup(name='webapp',
        version='1.0',
        description='A web application',
        author='John Doe',
        author_email='john@doe.com',
        url='https://doe.com/app',
        zip_safe=False,
        package_dir={'': './'},
        packages=['webapp'],
        install_requires=[])

