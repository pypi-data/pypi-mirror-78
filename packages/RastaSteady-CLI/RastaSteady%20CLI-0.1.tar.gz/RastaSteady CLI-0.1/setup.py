from setuptools import setup

setup(
    name='RastaSteady CLI',
    version='0.1',
    py_modules=['rastasteady-cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        rastasteady=cli:cli
        rastasteady-cli=cli:cli
    ''',
)
