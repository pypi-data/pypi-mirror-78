import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loginpy", 
    version="0.0.2",
    author="SnowCode", 
    description="A simple Flask library to make login management easier.", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.com/chopin42/login.py", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
