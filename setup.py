from setuptools import setup, find_packages

setup(
    name="tfchkr",
    version="0.1",
    description="tfchkr is a tool to help test Terraform modules and files.",
    author="Tucker McCoy",
    author_email="tuckermmccoy@gmail.com",
    keywords="terraform test compliance python",
    packages=find_packages(exclude=["tests"]),
    install_requires=["Click==7.0", "colorama==0.4.3", "checkov==1.0.550"],
    entry_points={"console_scripts": ["tfchkr=src.main:cli"]},
)
