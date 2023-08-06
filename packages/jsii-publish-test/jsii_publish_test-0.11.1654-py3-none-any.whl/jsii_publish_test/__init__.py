"""
# JSII Publish Test

This is a test package, created by [JSII Publish](https://github.com/udondan/jsii-publish) to test the publishing functionality of the Docker image.

## Version description

* The package version is prefixed with the version of the Docker image.
* Next comes an identifier of the source:

  * 1: [GitHub Workflow](https://github.com/udondan/jsii-publish/blob/master/.github/workflows/pr-test.yml)
  * 2: TravisCI
  * 3: CircleCI
* A random number between 1 and 999

Example: Version 0.8.3**1**677 means it is the Docker image version 0.8.3, pushed from GitHub Workflow with a random number of 677.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_s3
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("jsii-publish-test", "0.11.1654", __name__, "jsii-publish-test@0.11.1654.jsii.tgz")


class Test(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="jsii-publish-test.Test"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(Test, self, [scope, id])


__all__ = ["Test", "__jsii_assembly__"]

publication.publish()
