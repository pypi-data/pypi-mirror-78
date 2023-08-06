from setuptools import setup, find_namespace_packages

setup(
    name='origo-devportal-poctools',
    version='0.0.6',
    author='Oslo Origo',
    author_email='developerportal@oslo.kommune.no',
    description='A set of tools and models used by all parts of the harvest poc',
    project_urls={
        'Bug Tracker': 'https://github.com/oslokommune/devportal-harvest-poc/issues',
        'Source Code': 'https://github.com/oslokommune/devportal-harvest-poc'
    },
    license='https://mit-license.org/',
    packages=find_namespace_packages(include='origo.*'),
    install_requires=[
        'pyyaml==5.3.1'
    ]
)
