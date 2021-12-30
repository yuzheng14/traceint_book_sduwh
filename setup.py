import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="traceint",
    version="1.3.6",
    author="yuzheng14",
    author_email="yuzheng14@yuzheng14.com",
    description="integrated assistance of traceint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuzheng14/tracient_book_sduwh",
    packages=setuptools.find_packages(),
    install_requires=['ddddocr>=1.1.0', 'requests>=2.26.0', 'websocket-client>=1.2.3'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
