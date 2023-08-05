"""
Setup script for the conwech package.
"""

import setuptools
import subprocess
import os
import re


long_description = 'Unable to access README.md during setup!'
if os.path.exists('README.md'):
    with open('README.md', 'r') as readme:
        long_description = readme.read()

# use latest tag as version
result = subprocess.run(
    ['git', 'describe', '--tags', '--abbrev=0'],
    capture_output=True, text=True, check=True)
version = re.match(
    r'v?(?P<tag>\w+(?:\.\w+)*)+',
    str(result.stdout)).groupdict()['tag']

setuptools.setup(
    name='conwech',
    version=version,
    author='Kevin Turner',
    author_email='kct0004@auburn.edu',
    description='A module for reading & writing numbers using the Conway-Wechsler naming system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KCATurner/conwech.git',
    packages=setuptools.find_packages(
        exclude=['tests*', ],
    ),
    install_requires=[
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'conwech = conwech.__main__:main',
        ],
    },
    python_requires='>=3.4',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
