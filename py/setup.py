from setuptools import setup, find_packages

setup(
    name='parashell',
    version='0.3.0',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'program = run:run',
        ],
    },
)
