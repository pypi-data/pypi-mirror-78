import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyru",
    version="0.0.0",
    author="Mattlau04, blakeando",
    author_email="None@mail.com",
    description="Pyru is a python api wrapper for multiple boorus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pyru-team/Pyru",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
