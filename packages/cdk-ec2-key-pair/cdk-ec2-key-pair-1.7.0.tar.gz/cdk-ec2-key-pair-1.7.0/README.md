# CDK EC2 Key Pair

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/cdk-ec2-key-pair)
[![Test](https://github.com/udondan/cdk-ec2-key-pair/workflows/Test/badge.svg)](https://github.com/udondan/cdk-ec2-key-pair/actions?query=workflow%3ATest)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-ec2-key-pair)](https://github.com/udondan/cdk-ec2-key-pair/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--ec2--key--pair-orange)](https://awscdk.io/packages/cdk-ec2-key-pair@1.7.0)

[![npm package](https://img.shields.io/npm/v/cdk-ec2-key-pair?color=brightgreen)](https://www.npmjs.com/package/cdk-ec2-key-pair)
[![PyPI package](https://img.shields.io/pypi/v/cdk-ec2-key-pair?color=brightgreen)](https://pypi.org/project/cdk-ec2-key-pair/)
[![NuGet package](https://img.shields.io/nuget/v/CDK.EC2.KeyPair?color=brightgreen)](https://www.nuget.org/packages/CDK.EC2.KeyPair/)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/cdk-ec2-key-pair?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-ec2-key-pair)
[![PyPI](https://img.shields.io/pypi/dm/cdk-ec2-key-pair?label=pypi&color=blueviolet)](https://pypi.org/project/cdk-ec2-key-pair/)
[![NuGet](https://img.shields.io/nuget/dt/CDK.EC2.KeyPair?label=nuget&color=blueviolet)](https://www.nuget.org/packages/CDK.EC2.KeyPair/)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing [EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

CloudFormation doesn't directly support creation of EC2 Key Pairs. This construct provides an easy interface for creating Key Pairs through a [custom CloudFormation resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html). The private key is stored in [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import aws_cdk.aws_ec2 as ec2
from cdk_ec2_key_pair import KeyPair

# Create the Key Pair
key = KeyPair(self, "A-Key-Pair",
    name="a-key-pair",
    description="This is a Key Pair"
)

# Grant read access to the private key to a role or user
key.grant_read(some_role)

# Use Key Pair on an EC2 instance
ec2.Instance(self, "An-Instance", {
    "key_name": key.name
})
```

The private key will be stored in AWS Secrets Manager. The secret name by default is prefixed with `ec2-private-key/`, so in this example it will be saved as `ec2-private-key/a-key-pair`.

To download the private key via AWS cli you can run:

```bash
aws secretsmanager get-secret-value \
  --secret-id ec2-private-key/a-key-pair \
  --query SecretString \
  --output text
```

## Roadmap

* Name should be optional
