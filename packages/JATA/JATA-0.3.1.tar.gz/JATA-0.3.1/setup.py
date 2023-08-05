import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
# populate list of all paths in `./pixplot_notebook/web`
web = []
for root, subdirs, files in os.walk(os.path.join('pixplot_notebook', 'web')):
    if not files: continue
    for file in files:
        web.append(os.path.join(root.replace('pixplot_notebook/', ''), file))
setuptools.setup(
    name="JATA",  # Replace with your own username
    version="0.3.1",
    author="Blaise Albis Burdige",
    author_email="albisbub@reed.edu",
    description="A Digital Humanities Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albisbub/JATA-TOOLS",
    packages=setuptools.find_namespace_packages(),
    package_data={
        'pixplot_notebook': web,
    },
    entry_points={
        'console_scripts': [
            'pixplot_notebook=pixplot:parse',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
