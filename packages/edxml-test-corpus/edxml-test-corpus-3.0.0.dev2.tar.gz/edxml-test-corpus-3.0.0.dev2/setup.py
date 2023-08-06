import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="edxml-test-corpus",
    version="3.0.0.dev2",
    author="Dik Takken",
    author_email="d.h.j.takken@edxml.org",
    description="A collection of portable unit tests for EDXML implementations",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/edxml/test-corpus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    package_data={
        'edxml_test_corpus': ['tests/*/*.edxml', 'tests/*/*/*.edxml', 'tests/*/*/*/*.edxml']
    },
)
