import sys

from setuptools import setup, find_packages
if sys.version_info < (3, 6):
    sys.exit('Python 3.6 or greater is required.')

extra_requirements = ()

LICENSE = "MIT"
VERSION = '0.1.3'

setup(
    name='gt-webcore',
    description='A Web Service Framework Base On Flask And Sqlalchemy',
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Genetalks/gt-webcore',
    version=VERSION,
    author='wunan',
    author_email='wunan799@163.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    keywords=['flask', 'sqlalchemy', 'restful'],
    license=LICENSE,
    packages=find_packages(exclude=['tests']),
    install_requires=(
        'Flask >= 1.1.2',
        'Flask-Cors >= 3.0.8',
        'Flask-SQLAlchemy >= 2.4.3',
        'SQLAlchemy >= 1.3.17',
        'PyMySQL >= 0.9.3',
        'flask-restful',
        'flexible-dotdict',
        'requests'
    ) + extra_requirements,
)

