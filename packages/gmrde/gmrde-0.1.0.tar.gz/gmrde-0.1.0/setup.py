from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name='gmrde',
	version='0.1.0',
	description='Analysieren und Umformen deutscher Wörter und Sätze',
	long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://github.com/jarinox/python-grammar-de',
	author='Jakob Stolze',
	author_email='jarinox@wolke7.de',
	license='LGPLv2.1',
	packages=['gmrde'],
    classifiers=[
        "Natural Language :: German",
        "Programming Language :: Python :: 3",
    ],
	include_package_data=True,
	python_requires='>=3.6',
	zip_safe=False
)
