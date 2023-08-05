from setuptools import setup, find_packages
import os
setup(
    name="pdb2py",
    version="1.0",
    packages=find_packages(),
    scripts=[],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["docutils>=0.3",'pidly'],
    data_files=[(root, [os.path.join(root, f) for f in files])
    for root, dirs, files in os.walk('pdb2py/libIDL')],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"],
        },

    # metadata to display on PyPI
    author="Jerome Guterl",
    author_email="guterlj@fusion.gat.com",
    description="Read a pdb file and return a dictionary",
    keywords="pdb uedge",
    url="",   # project home page, if any
    project_urls={
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]

)
