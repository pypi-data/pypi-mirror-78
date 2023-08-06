"""
# CloudFront Origins for the CDK CloudFront Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains convenience methods for defining origins for a CloudFront distribution. You can use this library to create origins from
S3 buckets, Elastic Load Balancing v2 load balancers, or any other domain name.

## S3 Bucket

An S3 bucket can be added as an origin. If the bucket is configured as a website endpoint, the distribution can use S3 redirects and S3 custom error
documents.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins

my_bucket = s3.Bucket(self, "myBucket")
cloudfront.Distribution(self, "myDist",
    default_behavior=BehaviorOptions(origin=origins.S3Origin(my_bucket))
)
```

The above will treat the bucket differently based on if `IBucket.isWebsite` is set or not. If the bucket is configured as a website, the bucket is
treated as an HTTP origin, and the built-in S3 redirects and error pages can be used. Otherwise, the bucket is handled as a bucket origin and
CloudFront's redirect and error handling will be used. In the latter case, the Origin wil create an origin access identity and grant it access to the
underlying bucket. This can be used in conjunction with a bucket that is not public to require that your users access your content using CloudFront
URLs and not S3 URLs directly.

## ELBv2 Load Balancer

An Elastic Load Balancing (ELB) v2 load balancer may be used as an origin. In order for a load balancer to serve as an origin, it must be publicly
accessible (`internetFacing` is true). Both Application and Network load balancers are supported.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2

vpc = ec2.Vpc(...)
# Create an application load balancer in a VPC. 'internetFacing' must be 'true'
# for CloudFront to access the load balancer and use it as an origin.
lb = elbv2.ApplicationLoadBalancer(self, "LB",
    vpc=vpc,
    internet_facing=True
)
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.LoadBalancerV2Origin(lb)}
)
```

The origin can also be customized to respond on different ports, have different connection properties, etc.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
origin = origins.LoadBalancerV2Origin(load_balancer,
    connection_attempts=3,
    connection_timeout=Duration.seconds(5),
    protocol_policy=cloudfront.OriginProtocolPolicy.MATCH_VIEWER
)
```

## From an HTTP endpoint

Origins can also be created from any other HTTP endpoint, given the domain name, and optionally, other origin properties.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.Distribution(self, "myDist",
    default_behavior={"origin": origins.HttpOrigin("www.example.com")}
)
```

See the documentation of `@aws-cdk/aws-cloudfront` for more information.

## Failover Origins (Origin Groups)

You can set up CloudFront with origin failover for scenarios that require high availability.
To get started, you create an origin group with two origins: a primary and a secondary.
If the primary origin is unavailable, or returns specific HTTP response status codes that indicate a failure,
CloudFront automatically switches to the secondary origin.
You achieve that behavior in the CDK using the `OriginGroup` class:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cloudfront.Distribution(self, "myDist",
    default_behavior={
        "origin": origins.OriginGroup(
            primary_origin=origins.S3Origin(my_bucket),
            fallback_origin=origins.HttpOrigin("www.example.com"),
            # optional, defaults to: 500, 502, 503 and 504
            fallback_status_codes=[404]
        )
    }
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_cloudfront
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_s3
import aws_cdk.core


class HttpOrigin(
    aws_cdk.aws_cloudfront.OriginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront-origins.HttpOrigin",
):
    """An Origin for an HTTP server or S3 bucket configured for website hosting.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        domain_name: str,
        *,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        protocol_policy: typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy] = None,
        read_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param domain_name: -
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)
        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = HttpOriginProps(
            http_port=http_port,
            https_port=https_port,
            keepalive_timeout=keepalive_timeout,
            protocol_policy=protocol_policy,
            read_timeout=read_timeout,
            connection_attempts=connection_attempts,
            connection_timeout=connection_timeout,
            custom_headers=custom_headers,
            origin_path=origin_path,
        )

        jsii.create(HttpOrigin, self, [domain_name, props])

    @jsii.member(jsii_name="renderCustomOriginConfig")
    def _render_custom_origin_config(
        self
    ) -> typing.Optional[aws_cdk.aws_cloudfront.CfnDistribution.CustomOriginConfigProperty]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "renderCustomOriginConfig", [])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront-origins.HttpOriginProps",
    jsii_struct_bases=[aws_cdk.aws_cloudfront.OriginProps],
    name_mapping={
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_headers": "customHeaders",
        "origin_path": "originPath",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "keepalive_timeout": "keepaliveTimeout",
        "protocol_policy": "protocolPolicy",
        "read_timeout": "readTimeout",
    },
)
class HttpOriginProps(aws_cdk.aws_cloudfront.OriginProps):
    def __init__(
        self,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        protocol_policy: typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy] = None,
        read_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Properties for an Origin backed by an S3 website-configured bucket, load balancer, or custom HTTP server.

        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        self._values = {}
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if keepalive_timeout is not None:
            self._values["keepalive_timeout"] = keepalive_timeout
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times that CloudFront attempts to connect to the origin;

        valid values are 1, 2, or 3 attempts.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get("connection_attempts")

    @builtins.property
    def connection_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        Valid values are 1-10 seconds, inclusive.

        default
        :default: Duration.seconds(10)

        stability
        :stability: experimental
        """
        return self._values.get("connection_timeout")

    @builtins.property
    def custom_headers(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of HTTP header names and values that CloudFront adds to requests it sends to the origin.

        default
        :default: {}

        stability
        :stability: experimental
        """
        return self._values.get("custom_headers")

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        """The HTTP port that CloudFront uses to connect to the origin.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get("http_port")

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        """The HTTPS port that CloudFront uses to connect to the origin.

        default
        :default: 443

        stability
        :stability: experimental
        """
        return self._values.get("https_port")

    @builtins.property
    def keepalive_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies how long, in seconds, CloudFront persists its connection to the origin.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get("keepalive_timeout")

    @builtins.property
    def protocol_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy]:
        """Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin.

        default
        :default: OriginProtocolPolicy.HTTPS_ONLY

        stability
        :stability: experimental
        """
        return self._values.get("protocol_policy")

    @builtins.property
    def read_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get("read_timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpOriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerV2Origin(
    HttpOrigin,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloudfront-origins.LoadBalancerV2Origin",
):
    """An Origin for a v2 load balancer.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        load_balancer: aws_cdk.aws_elasticloadbalancingv2.ILoadBalancerV2,
        *,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        protocol_policy: typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy] = None,
        read_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param load_balancer: -
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)
        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = LoadBalancerV2OriginProps(
            http_port=http_port,
            https_port=https_port,
            keepalive_timeout=keepalive_timeout,
            protocol_policy=protocol_policy,
            read_timeout=read_timeout,
            connection_attempts=connection_attempts,
            connection_timeout=connection_timeout,
            custom_headers=custom_headers,
            origin_path=origin_path,
        )

        jsii.create(LoadBalancerV2Origin, self, [load_balancer, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront-origins.LoadBalancerV2OriginProps",
    jsii_struct_bases=[HttpOriginProps],
    name_mapping={
        "connection_attempts": "connectionAttempts",
        "connection_timeout": "connectionTimeout",
        "custom_headers": "customHeaders",
        "origin_path": "originPath",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "keepalive_timeout": "keepaliveTimeout",
        "protocol_policy": "protocolPolicy",
        "read_timeout": "readTimeout",
    },
)
class LoadBalancerV2OriginProps(HttpOriginProps):
    def __init__(
        self,
        *,
        connection_attempts: typing.Optional[jsii.Number] = None,
        connection_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        custom_headers: typing.Optional[typing.Mapping[str, str]] = None,
        origin_path: typing.Optional[str] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        keepalive_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        protocol_policy: typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy] = None,
        read_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Properties for an Origin backed by a v2 load balancer.

        :param connection_attempts: The number of times that CloudFront attempts to connect to the origin; valid values are 1, 2, or 3 attempts. Default: 3
        :param connection_timeout: The number of seconds that CloudFront waits when trying to establish a connection to the origin. Valid values are 1-10 seconds, inclusive. Default: Duration.seconds(10)
        :param custom_headers: A list of HTTP header names and values that CloudFront adds to requests it sends to the origin. Default: {}
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'
        :param http_port: The HTTP port that CloudFront uses to connect to the origin. Default: 80
        :param https_port: The HTTPS port that CloudFront uses to connect to the origin. Default: 443
        :param keepalive_timeout: Specifies how long, in seconds, CloudFront persists its connection to the origin. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(5)
        :param protocol_policy: Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin. Default: OriginProtocolPolicy.HTTPS_ONLY
        :param read_timeout: Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout. The valid range is from 1 to 60 seconds, inclusive. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        self._values = {}
        if connection_attempts is not None:
            self._values["connection_attempts"] = connection_attempts
        if connection_timeout is not None:
            self._values["connection_timeout"] = connection_timeout
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if keepalive_timeout is not None:
            self._values["keepalive_timeout"] = keepalive_timeout
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy
        if read_timeout is not None:
            self._values["read_timeout"] = read_timeout

    @builtins.property
    def connection_attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times that CloudFront attempts to connect to the origin;

        valid values are 1, 2, or 3 attempts.

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get("connection_attempts")

    @builtins.property
    def connection_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The number of seconds that CloudFront waits when trying to establish a connection to the origin.

        Valid values are 1-10 seconds, inclusive.

        default
        :default: Duration.seconds(10)

        stability
        :stability: experimental
        """
        return self._values.get("connection_timeout")

    @builtins.property
    def custom_headers(self) -> typing.Optional[typing.Mapping[str, str]]:
        """A list of HTTP header names and values that CloudFront adds to requests it sends to the origin.

        default
        :default: {}

        stability
        :stability: experimental
        """
        return self._values.get("custom_headers")

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        """The HTTP port that CloudFront uses to connect to the origin.

        default
        :default: 80

        stability
        :stability: experimental
        """
        return self._values.get("http_port")

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        """The HTTPS port that CloudFront uses to connect to the origin.

        default
        :default: 443

        stability
        :stability: experimental
        """
        return self._values.get("https_port")

    @builtins.property
    def keepalive_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies how long, in seconds, CloudFront persists its connection to the origin.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(5)

        stability
        :stability: experimental
        """
        return self._values.get("keepalive_timeout")

    @builtins.property
    def protocol_policy(
        self,
    ) -> typing.Optional[aws_cdk.aws_cloudfront.OriginProtocolPolicy]:
        """Specifies the protocol (HTTP or HTTPS) that CloudFront uses to connect to the origin.

        default
        :default: OriginProtocolPolicy.HTTPS_ONLY

        stability
        :stability: experimental
        """
        return self._values.get("protocol_policy")

    @builtins.property
    def read_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Specifies how long, in seconds, CloudFront waits for a response from the origin, also known as the origin response timeout.

        The valid range is from 1 to 60 seconds, inclusive.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get("read_timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerV2OriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_cloudfront.IOrigin)
class OriginGroup(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront-origins.OriginGroup"
):
    """An Origin that represents a group.

    Consists of a primary Origin,
    and a fallback Origin called when the primary returns one of the provided HTTP status codes.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        fallback_origin: aws_cdk.aws_cloudfront.IOrigin,
        primary_origin: aws_cdk.aws_cloudfront.IOrigin,
        fallback_status_codes: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> None:
        """
        :param fallback_origin: The fallback origin that should serve requests when the primary fails.
        :param primary_origin: The primary origin that should serve requests for this group.
        :param fallback_status_codes: The list of HTTP status codes that, when returned from the primary origin, would cause querying the fallback origin. Default: - 500, 502, 503 and 504

        stability
        :stability: experimental
        """
        props = OriginGroupProps(
            fallback_origin=fallback_origin,
            primary_origin=primary_origin,
            fallback_status_codes=fallback_status_codes,
        )

        jsii.create(OriginGroup, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, *, origin_id: str
    ) -> aws_cdk.aws_cloudfront.OriginBindConfig:
        """The method called when a given Origin is added (for the first time) to a Distribution.

        :param scope: -
        :param origin_id: The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        stability
        :stability: experimental
        """
        options = aws_cdk.aws_cloudfront.OriginBindOptions(origin_id=origin_id)

        return jsii.invoke(self, "bind", [scope, options])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront-origins.OriginGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "fallback_origin": "fallbackOrigin",
        "primary_origin": "primaryOrigin",
        "fallback_status_codes": "fallbackStatusCodes",
    },
)
class OriginGroupProps:
    def __init__(
        self,
        *,
        fallback_origin: aws_cdk.aws_cloudfront.IOrigin,
        primary_origin: aws_cdk.aws_cloudfront.IOrigin,
        fallback_status_codes: typing.Optional[typing.List[jsii.Number]] = None,
    ) -> None:
        """Construction properties for {@link OriginGroup}.

        :param fallback_origin: The fallback origin that should serve requests when the primary fails.
        :param primary_origin: The primary origin that should serve requests for this group.
        :param fallback_status_codes: The list of HTTP status codes that, when returned from the primary origin, would cause querying the fallback origin. Default: - 500, 502, 503 and 504

        stability
        :stability: experimental
        """
        self._values = {
            "fallback_origin": fallback_origin,
            "primary_origin": primary_origin,
        }
        if fallback_status_codes is not None:
            self._values["fallback_status_codes"] = fallback_status_codes

    @builtins.property
    def fallback_origin(self) -> aws_cdk.aws_cloudfront.IOrigin:
        """The fallback origin that should serve requests when the primary fails.

        stability
        :stability: experimental
        """
        return self._values.get("fallback_origin")

    @builtins.property
    def primary_origin(self) -> aws_cdk.aws_cloudfront.IOrigin:
        """The primary origin that should serve requests for this group.

        stability
        :stability: experimental
        """
        return self._values.get("primary_origin")

    @builtins.property
    def fallback_status_codes(self) -> typing.Optional[typing.List[jsii.Number]]:
        """The list of HTTP status codes that, when returned from the primary origin, would cause querying the fallback origin.

        default
        :default: - 500, 502, 503 and 504

        stability
        :stability: experimental
        """
        return self._values.get("fallback_status_codes")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OriginGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_cloudfront.IOrigin)
class S3Origin(
    metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudfront-origins.S3Origin"
):
    """An Origin that is backed by an S3 bucket.

    If the bucket is configured for website hosting, this origin will be configured to use the bucket as an
    HTTP server origin and will use the bucket's configured website redirects and error handling. Otherwise,
    the origin is created as a bucket origin and will use CloudFront's redirect and error handling.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        bucket: aws_cdk.aws_s3.IBucket,
        *,
        origin_path: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: -
        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        props = S3OriginProps(origin_path=origin_path)

        jsii.create(S3Origin, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self, scope: aws_cdk.core.Construct, *, origin_id: str
    ) -> aws_cdk.aws_cloudfront.OriginBindConfig:
        """The method called when a given Origin is added (for the first time) to a Distribution.

        :param scope: -
        :param origin_id: The identifier of this Origin, as assigned by the Distribution this Origin has been used added to.

        stability
        :stability: experimental
        """
        options = aws_cdk.aws_cloudfront.OriginBindOptions(origin_id=origin_id)

        return jsii.invoke(self, "bind", [scope, options])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloudfront-origins.S3OriginProps",
    jsii_struct_bases=[],
    name_mapping={"origin_path": "originPath"},
)
class S3OriginProps:
    def __init__(self, *, origin_path: typing.Optional[str] = None) -> None:
        """Properties to use to customize an S3 Origin.

        :param origin_path: An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin. Must begin, but not end, with '/' (e.g., '/production/images'). Default: '/'

        stability
        :stability: experimental
        """
        self._values = {}
        if origin_path is not None:
            self._values["origin_path"] = origin_path

    @builtins.property
    def origin_path(self) -> typing.Optional[str]:
        """An optional path that CloudFront appends to the origin domain name when CloudFront requests content from the origin.

        Must begin, but not end, with '/' (e.g., '/production/images').

        default
        :default: '/'

        stability
        :stability: experimental
        """
        return self._values.get("origin_path")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3OriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpOrigin",
    "HttpOriginProps",
    "LoadBalancerV2Origin",
    "LoadBalancerV2OriginProps",
    "OriginGroup",
    "OriginGroupProps",
    "S3Origin",
    "S3OriginProps",
]

publication.publish()
