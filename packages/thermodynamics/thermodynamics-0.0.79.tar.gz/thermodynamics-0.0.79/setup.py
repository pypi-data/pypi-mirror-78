import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thermodynamics",
    version="0.0.79",
    author="Luis Zepeda",
    author_email="luiszepedavarela@comunidad.unam.mx",
    description="Thermodynamic calculations for pure substance and mixtures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luis-zepeda/thermodynamics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'scipy', 'matplotlib'],
)