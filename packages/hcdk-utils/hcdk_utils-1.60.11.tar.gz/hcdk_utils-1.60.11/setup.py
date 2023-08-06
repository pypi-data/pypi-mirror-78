from setuptools import setup, find_packages

CDK_VERSION = "1.60.0"

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='hcdk_utils',
    version='1.60.11',

    description="General utility library for CDK projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sentiampc/hcdk-utils",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,

    install_requires=[
        f"aws-cdk.core>={CDK_VERSION}",
        f"aws-cdk.aws_ec2>={CDK_VERSION}",
        f"aws-cdk.aws_sns>={CDK_VERSION}",
        f"aws-cdk.aws_cloudwatch>={CDK_VERSION}",
        f"aws-cdk.aws_cloudwatch_actions>={CDK_VERSION}",
        f"aws-cdk.aws-secretsmanager>={CDK_VERSION}",
        f"aws-cdk.aws_docdb>={CDK_VERSION}",
        f"aws-cdk.aws_rds>={CDK_VERSION} ",
        "deepmerge",
        "pyyaml"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
