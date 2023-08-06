from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='hcdk_utils',
    version='1.60.9',

    description="General utility library for CDK projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sentiampc/hcdk-utils",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws_ec2",
        "aws-cdk.aws_sns",
        "aws-cdk.aws_cloudwatch",
        "aws-cdk.aws_cloudwatch_actions",
        "aws-cdk.aws-secretsmanager",
        "deepmerge",
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
