import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fakenamegeneratorAPI",
    python_requires=">=3.7",
    version="0.0.5",
    packages=setuptools.find_packages(),
    url="https://github.com/catarium/fakenamegenerator_API",
    license="Apache-2.0 License",
    author="Catarium",
    author_email="tartarxan@gmail.com",
    description="my version of fakenamegenerator API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests~=2.24.0",
        "beautifulsoup4~=4.9.1",],
    include_package_data=False,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
    ],
)
