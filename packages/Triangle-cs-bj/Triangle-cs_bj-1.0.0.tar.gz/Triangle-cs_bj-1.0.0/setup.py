import setuptools
def readme():
    with open("README.md.txt","r") as f:
        return f.read()
setuptools.setup(
    name="Triangle-cs_bj", 
    version="1.0.0",
    author="B.Ajay",
    author_email="badhrinr@gmail.com",
    description="A Python module to compute Triangle stuff",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
