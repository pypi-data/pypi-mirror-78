import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_package", 
    version="0.0.1",
    # version number must be updated before every new release to PyPI
    author="Aahnik Daw",
    author_email="meet.aahnik@gmail.com",
    description="This is a template repository for creating python packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aahnik/py_package",
    packages=setuptools.find_packages(),

    install_requires=[],
    # the package names specified in the install requires list will automatically be installed
    # whenever somebody installs this package via pip

    package_data={'py_package': ['data/*']},
    # all files within the data sub-directory of this python package will be treated as data files

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
    # make sure to use correct python version
)

