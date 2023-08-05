from setuptools import setup
from glob import glob
exec(open('foo_bar_doo/version.py').read())
setup(name='foo-bar-doo',
    version=__version__,
    description='foo-bar-doo',
    url='https://github.com/grindsa/foo-bar-doo',
    author='grindsa',
    author_email='grindelsack@gmail.com',
    license='GPL',
    packages=['foo_bar_doo'],
    platforms='any',
    install_requires=[
        'mechanicalsoup',
        'bs4',
        'html5lib',
        'six'
    ],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: German',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    zip_safe=False,
    test_suite="test")
