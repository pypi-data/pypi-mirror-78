import setuptools
from version import __version__

with open("README.md", "r") as fh:
    LONG_DESC = fh.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = [
        l.strip() for l in f.readlines()
        if (
                len(l.strip()) > 0 and
                not l.strip().startswith("#")
        )
    ]

setuptools.setup(
        name=f"ist-pulse-data-extractor",
        version=__version__,
        author="Joe Goulet",
        author_email="support@istresearch.com",
        description="Pulse Data Extractor",
        long_description=LONG_DESC,
        long_description_content_type="text/markdown",
        url="https://github.com/istresearch/pulse-data-extractor",
        packages=["pulse.downloader"],
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=REQUIREMENTS,
        include_package_data=True,
    )



