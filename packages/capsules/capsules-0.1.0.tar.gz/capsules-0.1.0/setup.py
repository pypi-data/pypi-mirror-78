from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="capsules",
    version="0.1.0",
    packages=["capsules",],
    install_requires=[],
    license="MIT",
    url="https://github.com/reity/capsules",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Library for depositing a function definition "+\
                "inside a temporary module file.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
