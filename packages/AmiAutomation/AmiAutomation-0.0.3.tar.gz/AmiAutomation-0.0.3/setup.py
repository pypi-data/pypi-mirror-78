import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AmiAutomation", # Replace with your own username
    version="0.0.3",
    author="AMI",
    author_email="luis.castro@amiauomation.com",
    description="Package to extract samples into pandas dataframes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.6',
    data_files=[('DLLs\\',["Kernel.Message.dll","DigitArcPX3.Tools.DataToPython.dll","ICSharpCode.SharpZipLib.dll"])],
    install_requires=['pandas>=1.1.0','pythonnet>=2.5.1'],
    )