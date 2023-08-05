from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="mgclipboard",
    version="0.3.0",
    author="Eugen Ciur",
    author_email="eugen@papermerge.com",
    url="https://github.com/papermerge/mg-clipboard",
    description=("Clipboard middleware for Papermerge DMS"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0 License",
    keywords="Middleware, Django, Papermerge, DMS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
