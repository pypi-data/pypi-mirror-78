import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anysentiment", 
    version="0.0.1",
    author="Arghadeep Chaudhury",
    author_email="arghadeep.chaudhury@gmail.com",
    description="Python Lib For doing sentiment Analysis in Any Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deepstartup/anysentiment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)