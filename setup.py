#############################################
# File Name: setup.py
# Author: dtb
# Mail: 1750352866@qq.com
# Created Time: 2019-8-28
#############################################

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def get_requires_list(*file_paths):
    f = read(*file_paths)
    data = f.split("\n")
    return data


def setup():
    from setuptools import setup, find_packages

    setup(
        name="dtb_tools",
        version="0.0.8",
        keywords=("pytools container"),
        description="python tools",
        long_description="python tools",
        license="MIT Licence",
        url="https://github.com/DaoBillTang/py_tools",
        author="dtb",
        author_email="1750352866@qq.com",
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        include_package_data=True,
        platforms="any",
        install_requires=get_requires_list("requirements.txt")
    )


if __name__ == "__main__":
    """
    python setup.py installer -dev
    or 
    python setup.py setup -dev bdist_wheel 
    """
    setup()
