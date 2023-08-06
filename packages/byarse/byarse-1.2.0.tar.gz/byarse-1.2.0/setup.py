import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


packages = setuptools.find_packages()



setuptools.setup(
    name="byarse",
    version="1.2.0",
    author="Netriza",
    author_email="info@netriza.ml",
    description="Serialize Arguments as Bytes!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/netriza/byarse",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
