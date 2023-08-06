"""Packaging utility for CMCC DIASAPI"""


# https://packaging.python.org/tutorials/packaging-projects/
# https://packaging.python.org/discussions/install-requires-vs-requirements/
# https://pypi.org/classifiers/
# https://setuptools.readthedocs.io/en/latest/setuptools.html

# Run this file with the command:
# $ python setup.py install


import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='diasapi',
    version='0.4a1',
    author='Marco Mancini',
    author_email='marco.mancini@cmcc.it',
    description=('Python Client Library for accessing CMCC data'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=('https://github.com/CMCC-Foundation/CMCC-DIAS-Client/'
         'diasapi/diasapi'),
    packages=setuptools.find_packages(),
    install_requires=[
        'requests==2.23.0',
        'xarray==0.15.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Hydrology'
    ],
    python_requires='>=3.7',
    license='Apache License, Version 2.0'
)
