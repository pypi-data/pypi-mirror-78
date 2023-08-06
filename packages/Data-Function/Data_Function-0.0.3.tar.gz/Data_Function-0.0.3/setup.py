import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Data_Function", # Replace with your own username
    version="0.0.3",
    author="TIXhjq",
    author_email="hjq1922451756@gmail.com",
    description="kon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TIXhjq/CTR_Function",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.6',
)