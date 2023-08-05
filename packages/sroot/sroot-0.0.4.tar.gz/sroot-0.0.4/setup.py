import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    
    name="sroot",
 
    
    version="0.0.4",
 
    
    author="Aratrik Banerjee",
 
    
    author_email="baratrik@gmail.comm",
 
    
    description="sroot is a Python library for dealing with square root in radical form.",
 
    long_description=long_description,
 
    
    long_description_content_type="text/markdown",
 

    py_modules=["sroot"],

    package_dir={'':'src'},
 
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
