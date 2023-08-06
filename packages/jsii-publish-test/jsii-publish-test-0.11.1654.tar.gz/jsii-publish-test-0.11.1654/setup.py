import json
import setuptools

kwargs = json.loads("""
{
    "name": "jsii-publish-test",
    "version": "0.11.1654",
    "description": "A dummy construct, used for automated testing of jsii-publish",
    "license": "MIT",
    "url": "https://github.com/udondan/jsii-publish",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "project_urls": {
        "Source": "https://github.com/udondan/jsii-publish.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "jsii_publish_test",
        "jsii_publish_test._jsii"
    ],
    "package_data": {
        "jsii_publish_test._jsii": [
            "jsii-publish-test@0.11.1654.jsii.tgz"
        ],
        "jsii_publish_test": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.21.1",
        "publication>=0.0.3",
        "aws-cdk.aws-s3==1.20.0",
        "aws-cdk.core==1.20.0"
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
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
