# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.CfnInclude.html).

## Basic usage

Assume we have a file with an existing template.
It could be in JSON format, in a file `my-template.json`:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

Or it could by in YAML format, in a file `my-template.yaml`:

```yaml
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: some-bucket-name
```

It can be included in a CDK application with the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.cloudformation_include as cfn_inc

cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

Or, if your template uses YAML:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.yaml"
)
```

This will add all resources from `my-template.json` / `my-template.yaml` into the CDK application,
preserving their original logical IDs from the template file.

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3

cfn_bucket = cfn_template.get_resource("Bucket")
```

Note that any resources not present in the latest version of the CloudFormation schema
at the time of publishing the version of this module that you depend on,
including [Custom Resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html),
will be returned as instances of the class `CfnResource`,
and so cannot be cast to a different resource type.

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

If you need, you can also convert the CloudFormation resource to a higher-level
resource by importing it:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)
```

## Parameters

If your template uses [CloudFormation Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

param = cfn_template.get_parameter("MyParameter")
```

The `CfnParameter` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
param.default = "MyDefault"
```

You can also provide values for them when including the template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
inc.CfnInclude(stack, "includeTemplate",
    template_file="path/to/my/template",
    parameters={
        "MyParam": "my-value"
    }
)
```

This will replace all references to `MyParam` with the string 'my-value',
and `MyParam` will be removed from the Parameters section of the template.

## Conditions

If your template uses [CloudFormation Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

condition = cfn_template.get_condition("MyCondition")
```

The `CfnCondition` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
condition.expression = core.Fn.condition_equals(1, 2)
```

## Mappings

If your template uses [CloudFormation Mappings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/mappings-section-structure.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

mapping = cfn_template.get_mapping("MyMapping")
```

The `CfnMapping` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
mapping.set_value("my-region", "AMI", "ami-04681a1dbd79675a5")
```

## Rules

If your template uses [Service Catalog template Rules](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/reference-template_constraint_rules.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

rule = cfn_template.get_rule("MyRule")
```

The `CfnRule` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
rule.add_assertion(core.Fn.condition_contains(["m1.small"], my_parameter.value), "MyParameter has to be m1.small")
```

## Outputs

If your template uses [CloudFormation Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

output = cfn_template.get_output("MyOutput")
```

The `CfnOutput` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
output.value = cfn_bucket.attr_arn
```

## Nested Stacks

This module also support templates that use [nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html).

For example, if you have the following parent template:

```json
{
  "Resources": {
    "ChildStack": {
      "Type": "AWS::CloudFormation::Stack",
      "Properties": {
        "TemplateURL": "https://my-s3-template-source.s3.amazonaws.com/child-stack.json"
      }
    }
  }
}
```

where the child template pointed to by `https://my-s3-template-source.s3.amazonaws.com/child-stack.json` is:

```json
{
  "Resources": {
    "MyBucket": {
      "Type": "AWS::S3::Bucket"
    }
  }
}
```

You can include both the parent stack and the nested stack in your CDK application as follows:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
parent_template = inc.CfnInclude(stack, "ParentStack",
    template_file="path/to/my-parent-template.json",
    nested_stacks={
        "ChildStack": {
            "template_file": "path/to/my-nested-template.json"
        }
    }
)
```

The included nested stack can be accessed with the `getNestedStack` method:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
included_child_stack = parent_template.get_nested_stack("ChildStack")
child_stack = included_child_stack.stack
child_template = included_child_stack.included_template
```

Now you can reference resources from `ChildStack` and modify them like any other included template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket = child_template.get_resource("MyBucket")
cfn_bucket.bucket_name = "my-new-bucket-name"

role = iam.Role(child_stack, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)

role.add_to_policy(iam.PolicyStatement(
    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"
    ],
    resources=[cfn_bucket.attr_arn]
))
```
