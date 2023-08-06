import setuptools
#from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rewrite",
    version="0.0.1.dev5",
    author="Michael Barnard",
    author_email="mbarnard10@ivytech.edu",
    description="ReWrite is a Python package for generating PDF documents via LaTeX. The goal of this project is to allow instructors to recreate course documents that must change in routine ways every time the course is offered. My vision is for ReWrite to support the creating of randomizable math problems and assessments without extensive programming knowledge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/rewrite/",
    packages=setuptools.find_packages(),
    scripts=[
        'bin/newproblem',
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
