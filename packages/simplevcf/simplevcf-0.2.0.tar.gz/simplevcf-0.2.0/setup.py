import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplevcf",  # Replace with your own username
    version="0.2.0",
    author="Yasunobu Okamura",
    author_email="okamura@informationsea.info",
    description="A simple VCF parser/weriter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/informationsea/simplevcf-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    python_requires='>=3.6',
)
