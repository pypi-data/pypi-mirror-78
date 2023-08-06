import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="adcopen",
    version="1.0.0",
    description="Open-source python libraries for data integration with ADC equipment.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://adc360.visualstudio.com/ADCOpen/_git/adcopen-python",
    author="Automated Design Corp.",
    author_email="support@automateddesign.com",
    license="Proprietary License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",        
        'License :: Other/Proprietary License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    packages=["adcopen"],
    include_package_data=True,
    install_requires=["nidaqmx", "numpy", "pandas", "ctypes", "time", "enum", "pywin32"]
)