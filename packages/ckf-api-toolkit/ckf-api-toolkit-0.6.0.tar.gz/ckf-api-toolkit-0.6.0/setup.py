import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ckf-api-toolkit",
    version="0.6.0",
    author="John Marian",
    author_email="john@johninthecloud.com",
    description="Tools for rapid deployment of REST API serverless applications using Python 3.7",
    install_requires=[
      "boto3",
      "requests"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cloud-kung-fu/ckf-api-toolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
