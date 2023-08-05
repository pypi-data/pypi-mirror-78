from setuptools import setup, find_packages

setup(
    name="stringhelper", 
    version="3.0",
    author_email="none@example.com",
    description="A small example package made to help you with strings",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)