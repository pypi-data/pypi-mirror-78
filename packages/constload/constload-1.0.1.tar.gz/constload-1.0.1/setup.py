import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="constload",
    version="1.0.1",
    author="Thomas Pain",
    author_email="tom@tdpain.net",
    description="A package to streamline constant loading and initialisation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.github.com/codemicro/constload",
    packages=["constload"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    install_requires=[],
    extras_require = {"yaml": ["PyYAML"]}
)