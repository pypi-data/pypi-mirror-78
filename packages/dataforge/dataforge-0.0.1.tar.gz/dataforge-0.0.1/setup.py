from setuptools import setup, find_namespace_packages

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='dataforge',
    version='0.0.1',
    author='Phil Schumm',
    author_email='pschumm@uchicago.edu',
    description='Tools for creating and packaging data products',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://gitlab.com/phs-rcg/data-forge',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'click>=7.1.2',
        'pandas>=1.0.4',
        'keyring>=21.2.1',
        'xmarshal>=0.0.1b1'
    ],
    entry_points='''
        [console_scripts]
        redcap_export=dataforge.sources.redcap.api:export
    ''',
)
