import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rds_cognito_attributes", # Replace with your own username
    version="0.0.2",
    author="Brandon Rosenbloom",
    author_email="brandonrosenbloom@gmail.com",
    description="A small package which can be used to query user information from both AWS Cognito and AWS Aurora RDS.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brandonrosenbloom/RDS_Cognito_attribute_alignment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)