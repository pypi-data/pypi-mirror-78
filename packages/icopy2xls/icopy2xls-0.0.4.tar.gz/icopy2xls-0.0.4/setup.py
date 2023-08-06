import setuptools

if __name__ == '__main__':
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="icopy2xls",
        version="0.0.4",
        author="Bernhard Buhl",
        author_email="info@baangt.org",
        description="Append rows of one Excel sheet to another, if header lines fit",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://baangt.org",
        packages=setuptools.find_packages(),
        data_files=[],
        package_data={},
        install_requires=["xlrd3", "openpyxl"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        include_package_data=True,
        python_requires='>=3.6',
    )
