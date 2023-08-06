import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="limpapat",
    version="0.0.2",
    author="Limpapat Bussaban",
    author_email="lim.bussaban@gmail.com",
    description="A collection of my codes",
    long_description="A collection of my codes",
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['torch'],
)