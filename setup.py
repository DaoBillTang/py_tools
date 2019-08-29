#############################################
# File Name: setup.py
# Author: dtb
# Mail: 1750352866@qq.com
# Created Time: 2019-8-28
#############################################

import codecs
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def get_build(*file_path):
    build_file = read(*file_path)
    import json

    build_json = json.loads(build_file)
    return build_json


def get_requires_list(*file_paths):
    f = read(*file_paths)
    data = f.split("\n")
    return data


def setup(build):
    from setuptools import setup, find_packages

    setup(
        name="dtb_tools",
        version="0.0.1",
        keywords=("pytools"),
        description="python tools",
        long_description="python tools",
        license="MIT Licence",
        url="https://github.com/fengmm521/pipProject",
        author="mage",
        author_email="mage@woodcol.com",

        packages=find_packages(),
        include_package_data=True,
        platforms="any",
        install_requires=[]
    )

    setup(
        name=build["__model_name__"],
        version=build["__version__"],
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        description=build["__description__"],
        install_requires=get_requires_list("requirements.txt"),
        include_package_data=True,
    )


def main():
    import datetime

    st = datetime.datetime.now()
    p = sys.argv[2]

    if p == "-ivt":
        print("正在进行测试版打包工作……")
    elif p == "-prod":
        print("正在进行正式版打包工作……")
    else:
        print("Error:错误的打包指令")
        sys.exit(1)
    build = get_build("build{0}.json".format(p))
    sys.argv.remove(p)
    p1 = sys.argv[1]

    if p1 == "setup":
        sys.argv.remove(p1)
        setup(build)
    else:
        print("无效命令")

    if sys.argv[-1] != "build":
        import shutil

        shutil.rmtree(os.path.abspath("build"))

    et = datetime.datetime.now()

    print("打包完成")
    print("耗时{0}".format(et - st))


if __name__ == "__main__":
    """
    python setup.py installer -dev
    or 
    python setup.py setup -dev bdist_wheel 
    """
    main()
