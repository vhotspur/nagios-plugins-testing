#!/usr/bin/env python3

from setuptools import setup

def get_readme():
    with open('README') as f:
        return f.read()

setup(
    name='d3s-nagios-plugins',
    version='0.1',
    description='Set of plugins from D3S',
    long_description=get_readme(),
    classifiers=[
      'Programming Language :: Python :: 3.6',
    ],
    keywords='nagios monitoring',
    url='https://lab.d3s.mff.cuni.cz/nagios-plugins/',
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    packages=[
        'd3s',
        'd3s.nagios_plugins',
    ],
    entry_points={
        'console_scripts': [
            'nagios_d3s_check_health=d3s.nagios_plugins.check_health',
            'nagios_d3s_check_systemd_service=d3s.nagios_plugins.check_systemd_service',
        ],
    },
)
