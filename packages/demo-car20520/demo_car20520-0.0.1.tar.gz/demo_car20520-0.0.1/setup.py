import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="demo_car20520",
    version="0.0.1",
    author="Hossam hassan",
    author_email="hossamhassan889@gmail.com",
    description="A demo_car package for test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/umeshdhakar/sample-python-package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
