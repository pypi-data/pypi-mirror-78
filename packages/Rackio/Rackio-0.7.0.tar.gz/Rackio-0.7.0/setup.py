# setup.py

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rackio",
    version="0.7.0",
    author="Nelson Carrasquel",
    author_email="rackio.framework@outlook.com",
    description="A modern Python Framework for microboard automation and control applications development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/rack-io/rackio-framework",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        'falcon',
        'pyBigParser',
        'peewee',
        'python-statemachine',
		'APScheduler',
        'Jinja2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
