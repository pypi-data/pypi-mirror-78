import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setuptools.setup(
    name="SPART-python",
    version="1.0.6",
    author="G. Worrall",
    author_email="worrall.george@gmail.com",
    description="Python implementation of the SPART optical radiative transfer model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wirrell/SPART-python",
    install_requires=parse_requirements('requirements.txt'),
    packages=setuptools.find_packages(),
    package_data={
        'SPART': ['model_parameters/*.pkl', 'sensor_information/*.pkl']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS"
    ],
    python_requires='>=3.4',
)
