from setuptools import setup, find_packages

setup(
    name='rastasteady',
    version='0.2.1',
    description='',
    long_description='',
    install_requires=[
        'pyfiglet',
        'click',
    ],
    entry_points='''
        [console_scripts]
        rastasteady=rastasteady.cli:cli
        rastasteady-cli=rastasteady.cli:cli
        rastasteady-web=rastasteady.web.web:web
    ''',
    packages=find_packages(),
    zip_safe=False,
)
