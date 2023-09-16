import setuptools

with open("README.md", "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="picstore",
    version="0.0.0",
    author="Nils Urbach",
    author_email="ndu01u@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=[],
    package_dir={"": "_core"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python"
    ],
    test_suite="tests",
)   