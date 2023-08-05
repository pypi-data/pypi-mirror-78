from setuptools import find_packages, setup

release_version = '0.1.2'

setup(
    name = 'ena-utils',
    version = release_version,
    description = 'A simple CLI toolbox to use the European Nucleotide Archive (ENA)',
    long_description = open('README.rst').read(),
    long_description_content_type = 'text/x-rst',
    license = 'Apache License 2.0',
    author = 'Laboratory of Integrative System Physiology (LISP) at EPFL',
    author_email = 'alexis.rapin@epfl.ch',
    url = 'https://github.com/auwerxlab/ena-utils',
    download_url = 'https://github.com/auwerxlab/ena-utils/archive/v' + release_version + '.tar.gz',
    packages = find_packages(),
    install_requires = [
        'click>=7.0',
        'pandas>=1.1.0',
        'xmltodict>=0.12.0',
    ],
    entry_points = {
        'console_scripts': [
            'ena-utils = ena_utils.__main__:cli'
        ]
    },
)
