
from operator import attrgetter
from os import path
from setuptools import setup

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name="wintoast",
    version="0.2",
    install_requires=["pypiwin32","setuptools"],
    packages=["wintoast"],
    license="BSD",
    url="https://github.com/samkenhuang/Windows-Toast-Notifications",
    download_url = 'https://github.com/samkenhuang/Windows-Toast-Notifications/0.2',
    description=(
        "An easy-to-use Python library for displaying "
        "Windows 10 Toast Notifications"
    ),
    include_package_data=True,
    package_data={
        '': ['*.txt'],
        'win10toast': ['data/*.ico'],
    },
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    author="Jithu R Jacob",
    author_email="=samkenhuang@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Operating System :: Microsoft',
        'Environment :: Win32 (MS Windows)',
        "License :: OSI Approved :: MIT License",
    ],
)
