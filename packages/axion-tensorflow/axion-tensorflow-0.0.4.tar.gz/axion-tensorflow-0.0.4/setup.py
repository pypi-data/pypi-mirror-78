import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="axion-tensorflow",  # Replace with your own username
    version="0.0.4",
    author="axion",
    author_email=" axion@aixin-chip.com",
    description="axion for TensorFlow >=2.2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aixin-chip/axion-tensorflow-models",
    packages=setuptools.find_packages(),
    install_requires=[
        "tensorflow>=2.2",
    ],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    license="Apache License 2.0",
    python_requires=">=3.5",
)
