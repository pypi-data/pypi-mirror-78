# coding: utf-8


from setuptools import setup  # noqa: H301

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
NAME = "pygitee"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="码云 Open API",
    author_email="",
    url="https://gitee.com/kingreatwill/pygitee",
    keywords=["Swagger", "码云 Open API"],
    install_requires=REQUIRES,
    packages=["gitee"],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
