from setuptools import setup, find_namespace_packages

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "VERSION")) as version_file:
    version = version_file.read().strip()

setup(
    name="mlderes.dstoolkit",
    version=version,
    description="A library of tools that I use to manage files,"
                "clean datasets and do exploratory data analysis",
    package_dir={"": "src"},
    # Telling the Disttools that the default directory is 'src'
    packages=find_namespace_packages(where="src", include="mlderes.*"),
    author="Michael Dereszynski",
    author_email="mlderes@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
