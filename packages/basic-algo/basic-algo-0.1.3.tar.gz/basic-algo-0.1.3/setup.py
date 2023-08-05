import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basic-algo",
    version="0.1.3",
    author="Harsh Chaplot, Kandarp Kakkad",
    author_email="17bit026@nirmauni.ac.in, 17bit034@nirmauni.ac.in",
    description="Using basic algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kandarpkakkad/BasicAlgo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
