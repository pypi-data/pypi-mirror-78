import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yorbali",
    version="0.0.2",
    author="Lalit Patel",
    author_email="llsr@att.net",
    description="Yorbali package for general-purpose data-processing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lapyl/yorbali",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)