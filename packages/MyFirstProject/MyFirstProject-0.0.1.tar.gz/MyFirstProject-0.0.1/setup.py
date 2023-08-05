import setuptools
import os
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir)))

with open("Readme","r") as f:
    long_description=f.read()

setuptools.setup(
    name="MyFirstProject",
    version="0.0.1",
    author="hf",
    author_email="",
    description="first",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    pr_modules=['ts'],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6'
)