import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-budget-notifier",
    "version": "0.2.3",
    "description": "@stefanfreitag/aws-budget-notifier",
    "license": "Apache-2.0",
    "url": "https://github.com/stefanfreitag/cdk-budget-notifier.git",
    "long_description_content_type": "text/markdown",
    "author": "Stefan Freitag<stefan@stefreitag.de>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/stefanfreitag/cdk-budget-notifier.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_budget_notifier",
        "cdk_budget_notifier._jsii"
    ],
    "package_data": {
        "cdk_budget_notifier._jsii": [
            "aws-budget-notifier@0.2.3.jsii.tgz"
        ],
        "cdk_budget_notifier": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-budgets==1.61.1",
        "aws-cdk.core==1.61.1",
        "constructs>=3.0.4, <4.0.0",
        "jsii>=1.12.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
"""
)

with open("README.md") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
