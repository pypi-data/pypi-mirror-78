import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="albus",
    version="0.0.2",
    author="Rafael Pivato",
    author_email="rafael@gotnotable.com",
    description="Small and dummy DB-API 2 data mapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gotnotable/albus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
)
