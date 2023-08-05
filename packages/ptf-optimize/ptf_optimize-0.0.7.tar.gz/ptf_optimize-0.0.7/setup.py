# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/

import setuptools


setuptools.setup(
    name="ptf_optimize", # Replace with your own username
    version="0.0.7",
    author="Juan Piao",
    author_email="juanpiao13@gmail.com",
    description="get optimal portfolio",
    
    long_description_content_type="text/markdown",
    url="https://github.com/JPL13",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False
)