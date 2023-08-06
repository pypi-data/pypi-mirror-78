## Amazon Redshift Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

### Starting a Redshift Cluster Database

To set up a Redshift cluster, define a `Cluster`. It will be launched in a VPC.
You can specify a VPC, otherwise one will be created. The nodes are always launched in private subnets and are encrypted by default.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_redshift as redshift
cluster = redshift.Cluster(self, "Redshift",
    master_user=Login(
        master_username="admin"
    ),
    vpc=vpc
)
```

By default, the master password will be generated and stored in AWS Secrets Manager.

A default database named `default_db` will be created in the cluster. To change the name of this database set the `defaultDatabaseName` attribute in the constructor properties.

### Connecting

To control who can access the cluster, use the `.connections` attribute. Redshift Clusters have
a default port, so you don't need to specify the port:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.connections.allow_from_any_ipv4("Open to the world")
```

The endpoint to access your database cluster will be available as the `.clusterEndpoint` attribute:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.cluster_endpoint.socket_address
```

### Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
