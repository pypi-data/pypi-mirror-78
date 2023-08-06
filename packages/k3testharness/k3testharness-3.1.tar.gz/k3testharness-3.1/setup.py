from setuptools import setup, find_packages

setup(
    name='k3testharness',
    version='3.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'k3testharness = k3testharness.test_harness:main'
        ]
    }
)