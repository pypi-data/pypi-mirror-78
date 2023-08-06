import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sca-fiuna", # Replace with your own username
    version="0.0.1",
    author="Jorge Tillería",
    author_email="jtilleria@fiuna.edu.py",
    description="Un paquete de uso para la materia de control en la FIUNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tetotille/SCA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.2',
)
