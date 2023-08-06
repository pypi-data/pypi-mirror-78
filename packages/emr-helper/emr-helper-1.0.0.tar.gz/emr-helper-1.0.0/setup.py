import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emr-helper",
    version="1.0.0",
    author="JevyanJ",
    author_email="jjrg184@gmail.com",
    description="Library to manage AWS EMR clusters.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/JevyanJ/emr-helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
