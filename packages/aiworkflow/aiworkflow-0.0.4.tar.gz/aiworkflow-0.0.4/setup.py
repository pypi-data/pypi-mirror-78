import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiworkflow",
    version="0.0.4",
    author="Pyxeda AI",
    author_email="support@pyxeda.ai",
    description="Python Client to access Navigator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://navigator.pyxeda.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
