"""
# cdk-url-shortener <!-- omit in toc -->

![Release](https://github.com/rayou/cdk-url-shortener/workflows/Release/badge.svg) [![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@rayou/cdk-url-shortener) [![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/rayou.cdk-url-shortener/)

> Deploy a URL shortener with custom domain support in just a few lines of code.

`cdk-url-shortener` is an AWS CDK L3 construct that will create a URL shortener with [custom domain](#custom-domain) support. The service uses [nanoid](https://github.com/ai/nanoid) to generate URL-friendly unique IDs and will retry if an ID collision occurs.

Additionally, you can enable [DynamoDB streams](#enable-dynamodb-streams) to capture changes to items stored in the DynamoDB table.

**Table of Contents**

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)

  * [Basic](#basic)
  * [Custom Domain](#custom-domain)
  * [Multiple Custom Domains](#multiple-custom-domains)
  * [Enable DynamoDB Streams](#enable-dynamodb-streams)
* [Create your first short URL](#create-your-first-short-url)
* [Documentation](#documentation)

  * [Construct API Reference](#construct-api-reference)
  * [URL Shortener API Endpoints](#url-shortener-api-endpoints)

    * [Shorten a Link](#shorten-a-link)
    * [Visit a shortened URL](#visit-a-shortened-url)
* [Supporting this project](#supporting-this-project)
* [License](#license)

## Features

* 🚀 Easy to Start - One-liner code to have your own URL shortener.
* 🏢 Custom Domain - Bring your custom domain name that fits your brand.
* 📡 DynamoDB Streams - Capture table activity with DynamoDB Streams.

## Installation

TypeScript/JavaScript

```sh
$ npm install @rayou/cdk-url-shortener
```

Python

```sh
$ pip install rayou.cdk-url-shortener
```

## Usage

### Basic

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from rayou.cdk_url_shortener import URLShortener

URLShortener(self, "myURLShortener")
```

### Custom Domain

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_certificatemanager as acm
from rayou.cdk_url_shortener import URLShortener

zone = route53.HostedZone.from_lookup(self, "HostedZone",
    domain_name="mydomain.com"
)

# Optional, a DNS validated certificate will be created if not provided.
certificate = acm.Certificate.from_certificate_arn(self, "Certificate", "arn:aws:acm:region:123456789012:certificate/12345678-1234-1234-1234-123456789012")

URLShortener(self, "myURLShortener").add_domain_name(
    domain_name="foo.mydomain.com",
    zone=zone,
    certificate=certificate
)
```

### Multiple Custom Domains

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as route53
from rayou.cdk_url_shortener import URLShortener

zone = route53.HostedZone.from_lookup(self, "HostedZone",
    domain_name="mydomain.com"
)

URLShortener(self, "myURLShortener").add_domain_name(
    domain_name="foo.mydomain.com",
    zone=zone
).add_domain_name(
    domain_name="bar.mydomain.com",
    zone=zone
)
```

⚠️ Please note that although we have added two custom domains, they are pointed to the same URL shortener instance sharing the same DynamoDB table, if you need both domains run independently, create a new URL shortener instance.

### Enable DynamoDB Streams

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_lambda_event_sources as lambda_event_sources

from rayou.cdk_url_shortener import URLShortener

table = dynamodb.Table(self, "Table",
    partition_key=Attribute(
        name="id",
        type=dynamodb.AttributeType.STRING
    ),
    stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
)

URLShortener(self, "myURLShortener",
    dynamo_table=table
)

stream_handler_code = "'use strict';\n    exports.handler = async (event) => {\n      console.log('Received event:', JSON.stringify(event, null, 2));\n      for (const record of event.Records) {\n        console.log(record.eventID);\n        console.log(record.eventName);\n        console.log('DynamoDB Record: %j', record.dynamodb);\n      }\n      console.log(`Successfully processed ${event.Records.length} records.`);\n    };"

lambda_fn = lambda_.Function(self, "myStreamHandler",
    runtime=lambda_.Runtime.NODEJS_12_X,
    handler="index.handler",
    code=lambda_.Code.from_inline(stream_handler_code)
)

lambda_fn.add_event_source(
    lambda_event_sources.DynamoEventSource(table,
        starting_position=lambda_.StartingPosition.LATEST
    ))
```

## Create your first short URL

1. After the deployment, you'll see `ApiKeyURL` and `ApiEndpoint` in CDK Outputs, visit `ApiKeyURL` to get your API key.

   ```shell
   Outputs:
   stack.CustomDomainApiEndpointcc4157 = https://mydomain.com
   stack.myURLShortenerApiEndpoint47185311 = https://yrzxcvbafk.execute-api.us-west-2.amazonaws.com/prod/
   stack.ApiKeyURL = https://console.aws.amazon.com/apigateway/home?#/api-keys/k2zxcvbafw6
   ```
2. Run this cURL command to create your first short URL, an `ID` will be returned in the response.

   ```sh
   $ curl https://{API_ENDPOINT} /
       -X POST \
       -H 'content-type: application/json' \
       -H 'x-api-key: {API_KEY}' \
       -d '{
         "url": "https://github.com/rayou/cdk-url-shortener"
       }'

   {"id":"LDkPh"}
   ```
3. Visit `https://{API_ENDPOINT}/{ID}` then you'll be redirected to the destination URL.

   ```sh
   $ curl -v https://{API_ENDPOINT}/{ID} # e.g. https://mydomain.com/LDkPh

   < HTTP/2 301
   < content-type: text/html; charset=UTF-8
   < content-length: 309
   < location: https://github.com/rayou/cdk-url-shortener

   <!DOCTYPE html><html><head><meta charset="UTF-8" /><meta http-equiv="refresh" content="0;url=https://github.com/rayou/cdk-url-shortener" /><title>Redirecting to https://github.com/rayou/cdk-url-shortener</title></head><body>Redirecting to <a href="https://github.com/rayou/cdk-url-shortener">https://github.com/rayou/cdk-url-shortener</a>.</body></html>
   ```

## Documentation

### Construct API Reference

See [API.md](./API.md).

### URL Shortener API Endpoints

#### Shorten a Link

**HTTP REQUEST**

`POST /`

**HEADERS**

| Name           | Value                      | Required |
| -------------- | -------------------------- | -------- |
| `content-type` | `application/json`         | Required |
| `x-api-key`    | Get your api key [here](https://console.aws.amazon.com/apigateway/home?#/api-keys) | Required |

**ARGUMENTS**

| Parameter | Type   | Required | Description     |
| --------- | ------ | -------- | --------------- |
| `url`     | string | Required | Destination URL |

**Example Request**

```sh
curl https://mydomain.com /
  -X POST \
  -H 'content-type: application/json' \
  -H 'x-api-key: v3rYsEcuRekey' \
  -d '{
    "url": "https://github.com/rayou/cdk-url-shortener"
  }'
```

**Response (201)**

```json
{
  "id": "LDkPh"
}
```

#### Visit a shortened URL

**HTTP REQUEST**

`GET /:id`

**Example Request**

```sh
curl https://mydomain.com/:id
```

**Response (301)**

```sh
< HTTP/2 301
< content-type: text/html; charset=UTF-8
< content-length: 309
< location: https://github.com/rayou/cdk-url-shortener

<!DOCTYPE html><html><head><meta charset="UTF-8" /><meta http-equiv="refresh" content="0;url=https://github.com/rayou/cdk-url-shortener" /><title>Redirecting to https://github.com/rayou/cdk-url-shortener</title></head><body>Redirecting to <a href="https://github.com/rayou/cdk-url-shortener">https://github.com/rayou/cdk-url-shortener</a>.</body></html>
```

## Supporting this project

I'm working on this project in my free time, if you like my project, or found it helpful and would like to support me, you can buy me a coffee, any contributions are much appreciated! ❤️

<a href="https://www.buymeacoffee.com/rayou" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>

## License

This project is distributed under the [Apache License, Version 2.0](./LICENSE).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_dynamodb
import aws_cdk.aws_route53
import aws_cdk.core


@jsii.data_type(
    jsii_type="@rayou/cdk-url-shortener.CustomDomainOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "zone": "zone",
        "certificate": "certificate",
    },
)
class CustomDomainOptions:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        zone: aws_cdk.aws_route53.IHostedZone,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
    ) -> None:
        """Properties to configure a domain name.

        :param domain_name: Domain name to be associated with URL shortener service, supports apex domain and subdomain.
        :param zone: Hosted zone of the domain which will be used to create alias record(s) from domain name in the hosted zone to URL shortener API endpoint.
        :param certificate: The AWS Certificate Manager (ACM) certificate that will be associated with the URL shortener that will be created. Default: - A new DNS validated certificate is created in the same region.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "domain_name": domain_name,
            "zone": zone,
        }
        if certificate is not None:
            self._values["certificate"] = certificate

    @builtins.property
    def domain_name(self) -> builtins.str:
        """Domain name to be associated with URL shortener service, supports apex domain and subdomain.

        stability
        :stability: experimental
        """
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return result

    @builtins.property
    def zone(self) -> aws_cdk.aws_route53.IHostedZone:
        """Hosted zone of the domain which will be used to create alias record(s) from domain name in the hosted zone to URL shortener API endpoint.

        stability
        :stability: experimental
        """
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return result

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """The AWS Certificate Manager (ACM) certificate that will be associated with the URL shortener that will be created.

        default
        :default: - A new DNS validated certificate is created in the same region.

        stability
        :stability: experimental
        """
        result = self._values.get("certificate")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class URLShortener(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@rayou/cdk-url-shortener.URLShortener",
):
    """Represents a URL shortener.

    Use ``addDomainName`` to configure a custom domain.

    By default, this construct will deploy:

    - An API Gateway API that can be accessed from a public endpoint.
    - A DynamoDB table for storing links.
    - A Lambda Function for shortening the link and storing it to DynamoDB table.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dynamo_table: typing.Optional[aws_cdk.aws_dynamodb.Table] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param dynamo_table: The DynamoDB table used for storing links. A static property ``defaultDynamoTableProps`` is exposed with default partition key set to ``id``. You can extend it for your own ``TableProps``. Default: - A new DynamoDB Table is created.

        stability
        :stability: experimental
        """
        props = URLShortenerProps(dynamo_table=dynamo_table)

        jsii.create(URLShortener, self, [scope, id, props])

    @jsii.member(jsii_name="addDomainName")
    def add_domain_name(
        self,
        *,
        domain_name: builtins.str,
        zone: aws_cdk.aws_route53.IHostedZone,
        certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate] = None,
    ) -> "URLShortener":
        """
        :param domain_name: Domain name to be associated with URL shortener service, supports apex domain and subdomain.
        :param zone: Hosted zone of the domain which will be used to create alias record(s) from domain name in the hosted zone to URL shortener API endpoint.
        :param certificate: The AWS Certificate Manager (ACM) certificate that will be associated with the URL shortener that will be created. Default: - A new DNS validated certificate is created in the same region.

        stability
        :stability: experimental
        """
        options = CustomDomainOptions(
            domain_name=domain_name, zone=zone, certificate=certificate
        )

        return jsii.invoke(self, "addDomainName", [options])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="defaultDynamoTableProps")
    def DEFAULT_DYNAMO_TABLE_PROPS(cls) -> aws_cdk.aws_dynamodb.TableProps:
        """Default table props with partition key set to ``id``, you can use it to extend your ``TableProps``.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            table_props = {
                (SpreadAssignment ...URLShortener.defaultDynamoTableProps
                  URLShortener.default_dynamo_table_props),
                "stream": StreamViewType.NEW_AND_OLD_IMAGES
            }
        """
        return jsii.sget(cls, "defaultDynamoTableProps")


@jsii.data_type(
    jsii_type="@rayou/cdk-url-shortener.URLShortenerProps",
    jsii_struct_bases=[],
    name_mapping={"dynamo_table": "dynamoTable"},
)
class URLShortenerProps:
    def __init__(
        self,
        *,
        dynamo_table: typing.Optional[aws_cdk.aws_dynamodb.Table] = None,
    ) -> None:
        """Properties to configure a URL shortener.

        :param dynamo_table: The DynamoDB table used for storing links. A static property ``defaultDynamoTableProps`` is exposed with default partition key set to ``id``. You can extend it for your own ``TableProps``. Default: - A new DynamoDB Table is created.

        stability
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if dynamo_table is not None:
            self._values["dynamo_table"] = dynamo_table

    @builtins.property
    def dynamo_table(self) -> typing.Optional[aws_cdk.aws_dynamodb.Table]:
        """The DynamoDB table used for storing links.

        A static property ``defaultDynamoTableProps`` is exposed with default
        partition key set to ``id``. You can extend it for your own ``TableProps``.

        default
        :default: - A new DynamoDB Table is created.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            table_props = {
                (SpreadAssignment ...URLShortener.defaultDynamoTableProps
                  URLShortener.default_dynamo_table_props),
                "stream": StreamViewType.NEW_AND_OLD_IMAGES
            }
        """
        result = self._values.get("dynamo_table")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "URLShortenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CustomDomainOptions",
    "URLShortener",
    "URLShortenerProps",
]

publication.publish()
