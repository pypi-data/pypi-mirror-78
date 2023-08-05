#!/usr/bin/env python
import os
import subprocess
from setuptools import setup, find_packages


version = '0.1.0a2'
sha = 'Unknown'
package_name = 'torch-io'

try:
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8') 
except Exception:
    pass

cwd = os.path.dirname(os.path.abspath(__file__))
version_path = os.path.join(cwd, 'torch_io', 'version.py')
with open(version_path, 'w') as f:
    f.write("__version__ = '{}'\n".format(version))
    f.write('git_version = {}'.format(repr(sha)))

readme = open('README.md').read()

requirements = open('requirements.txt').read().split()

setup(
    name=package_name,
    version=version,
    author='Omkar Prabhu',
    author_email='prabhuomkar@pm.me',
    url='https://github.com/prabhuomkar/io',
    description='TBD',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('tests', 'docs', 'examples', 'scripts')),
    zip_safe=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
)