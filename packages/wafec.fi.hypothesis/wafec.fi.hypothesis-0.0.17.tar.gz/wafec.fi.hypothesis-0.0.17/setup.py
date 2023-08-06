from setuptools import setup, find_packages

setup(
    packages=find_packages("src"),
    entry_points={
        'console_scripts': [
            'wafec-fi-hypothesis-models-create_all = wafec.fi.hypothesis.models.create_all:main',
            'wafec-fi-hypothesis-server = wafec.fi.hypothesis.server:main'
        ]
    }
)
