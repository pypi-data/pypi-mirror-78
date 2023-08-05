import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spectre_ai",
    version="0.0.2",
    author="Sebastian Willowhawk",
    author_email="bazindigo@gmail.com",
    description="Modules for Spectre AI Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bazindigo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Development Status :: 1 - Planning"
    ],
    python_requires='>=3.8',
)