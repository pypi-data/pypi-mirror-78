import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.1"

"""
https://docs.python.org/3/distutils/configfile.html
1. 打包
python setup.py sdist bdist_wheel
sdist - 构建源码分发包，在 Windows 下为 zip 格式，Linux 下为 tag.gz 格式 。
bdist - 构建一个二进制的分发包。
bdist_egg - 构建一个 egg 分发包，经常用来替代基于 bdist 生成的模式
2. 上传
python setup.py sdist upload

https://twine.readthedocs.io/en/latest/#installation
twine upload -u kingreatwill -p x dist/*
twine upload --config-file .pypirc dist/*
twine upload -u kingreatwill -p pypi-AgEIcHlwaS5vcmcCJDY2ZDlmNWM3LWZkYmEtNDI2MC1iZWJkLWQ0Mzk3NGM2YTZlMwACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgnaG82ck6jV4aToFoA3bWI3Ge4kxhcdwJsUYhudc8XrM dist/*
"""
if __name__ == "__main__":
    setuptools.setup(
        name="pygitee",
        version=version,
        description="Use the full gitee API v5",
        author="kingreatwill",
        author_email="kingreatwill@qq.com",
        url="https://gitee.com/kingreatwill/pygitee",
        packages=["gitee"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
    )
