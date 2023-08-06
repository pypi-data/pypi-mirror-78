import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whyis-unit-converter",
    version="0.0.2",
    author="Rory Schadler",
    author_email="rory.h.schadler.21@dartmouth.edu",
    description="Unit converter for Whyis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roryschadler/whyis_unit_converter",
    packages=['whyis_unit_converter', 'bin'],
    include_package_data=True,
    install_requires=['Pint',
                      'rdflib'],
    scripts=['bin/unitconvertertest', 'bin/importconverterdict'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2'
)
