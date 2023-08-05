import setuptools
from setuptools import Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-nim-pkg-stever",
    version="0.0.2",
    author="Steven Robertson",
    author_email="stever@hey.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
    	"": ["*.so", "*.pyd"]
    },
    include_package_data=True,
    zip_safe=False,
    ext_modules = [
        Extension(
            name = 'dummy',
            sources = ['dummy.c']
        )
    ]
)