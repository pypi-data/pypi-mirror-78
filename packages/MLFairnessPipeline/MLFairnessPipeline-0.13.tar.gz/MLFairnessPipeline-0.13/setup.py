import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='MLFairnessPipeline',
    version='0.13',
    scripts=['MLFairnessPipeline'] ,
    author="Mark Bentivegna",
    author_email="markbentivegna@gmail.com",
    description="An end to end ML Fairness Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markbentivegna/MLFairnessPipeline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)