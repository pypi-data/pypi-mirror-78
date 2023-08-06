import setuptools

with open("pyvis_inspector/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvis-inspector",
    version="0.0.1",
    license="MIT",
    author="Matthew Ashley",
    author_email="matthewashley@verntechnologies.com",
    description="A simple python wrapper for the IBM Vision Service API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewashley1/pyvis-inspector",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
