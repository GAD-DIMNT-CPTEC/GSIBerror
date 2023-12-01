from setuptools import setup, find_packages

setup(
    name='GSIBerror',
    version='1.2.1a1',
    url='https://gad-dimnt-cptec.github.io/GSIBerror',
    author='Carlos Frederico Bastarz',
    author_email='carlos.bastarz@inpe.br',
    description='A Python class to read the records and attributes from the background error covariance matrices compatible with the Gridpoint Statistical Interpolation (in the .gcv file format).',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'xarray',
        'cartopy',
        'matplotlib',
        ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
