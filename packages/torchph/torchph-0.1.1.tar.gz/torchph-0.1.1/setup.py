from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name="torchph",
    version="0.1.1",
    author="Sayantan Das",
    author_email="sayantandas30011998@gmail.com",
    description="torchph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/forkbabu/torchph",
    packages=find_packages(exclude=('tests*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='Persistent Homology',
)
