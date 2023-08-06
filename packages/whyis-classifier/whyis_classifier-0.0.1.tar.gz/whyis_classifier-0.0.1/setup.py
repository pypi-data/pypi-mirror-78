import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whyis_classifier",
    version="0.0.1",
    author="Rory Schadler",
    author_email="rory.h.schadler.21@dartmouth.edu",
    description="Classifier interface for Whyis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roryschadler/whyis_classifier",
    packages=['whyis_classifier', 'bin'],
    install_requires=['rdflib'],
    scripts=['bin/whyisclassifiertest'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2'
)
