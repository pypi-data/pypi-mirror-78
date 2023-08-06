from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="DP700",
    version="0.1",
    description="ARTIQ support for RIGOL DP700 series power supplies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OregonIons",
    url="https://github.com/ARTIQ-Controllers/DP700",
    download_url="https://github.com/ARTIQ-Controllers/DP700",
    license="LGPLv3+",
    install_requires=[
        "sipyco",
        "pyserial",
    ],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    entry_points={
        "console_scripts": [
            "aqctl_DP700 = DP700.aqctl_DP700:main",
        ],
    },
)