import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datefactory", 
    version="1.0.1",
    author="Niall Stapleton",
    author_email="niall.stapleton@gmail.com",
    description="Date Handling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    py_modules=["datefactory"],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
