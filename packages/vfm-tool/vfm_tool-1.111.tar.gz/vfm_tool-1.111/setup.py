'''Nicolas Trinephi - acse-nt719

Setup file for PyPI upload
'''

import setuptools
from distutils.core import setup


with open("README.md", "r") as f:
    long_description = f.read()

setup(
	name='vfm_tool',
	author='Nicolas Trinephi',
	author_email='nicolas.trinephi@imperial.ac.uk',
	version='1.111',
	description='Individual MSc Project',
	packages=['vfm_tool'],
	license='MIT',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/acse-2019/irp-acse-nt719/tree/master/Code/',
	include_package_data=True
	)