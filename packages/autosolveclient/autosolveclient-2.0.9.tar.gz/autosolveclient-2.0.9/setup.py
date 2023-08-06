import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autosolveclient",
    packages=['autosolveclient'],
    version="2.0.9",
    author="AYCD Inc",
    author_email="contact@aycd.io",
    description="Client for connecting to AYCD AutoSolve network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pika',
        'requests',
        'logzero',
        'pymitter'
    ],
    python_requires='>=3.6',
)