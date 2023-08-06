import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mbonig.nightynight",
    "version": "0.0.6",
    "description": "A CDK construct that will automatically stop a running EC2 instance at a given time.",
    "license": "MIT",
    "url": "https://github.com/mbonig/nightynight",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mbonig/nightynight"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.nightynight",
        "mbonig.nightynight._jsii"
    ],
    "package_data": {
        "mbonig.nightynight._jsii": [
            "nightynight@0.0.6.jsii.tgz"
        ],
        "mbonig.nightynight": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-ec2>=1.60.0, <2.0.0",
        "aws-cdk.aws-events-targets>=1.60.0, <2.0.0",
        "aws-cdk.aws-events>=1.60.0, <2.0.0",
        "aws-cdk.aws-iam>=1.60.0, <2.0.0",
        "aws-cdk.aws-lambda-nodejs>=1.60.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.60.0, <2.0.0",
        "aws-cdk.core==1.60.0",
        "cdk-iam-floyd>=0.54.1, <0.55.0",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.11.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
