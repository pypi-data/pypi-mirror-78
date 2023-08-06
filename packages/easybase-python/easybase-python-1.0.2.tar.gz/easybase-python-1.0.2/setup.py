import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easybase-python",
    version="1.0.2",
    author="EasyBase",
    author_email="hello@easybase.io",
    description="Python package for use with EasyBase.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/easybase/easybase-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)