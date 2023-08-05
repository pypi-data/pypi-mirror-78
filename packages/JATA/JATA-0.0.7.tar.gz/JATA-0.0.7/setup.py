import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JATA",  # Replace with your own username
    version="0.0.7",
    author="Blaise Albis Burdige",
    author_email="albisbub@reed.edu",
    description="A Digital Humanities Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albisbub/JATA-TOOLS",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
