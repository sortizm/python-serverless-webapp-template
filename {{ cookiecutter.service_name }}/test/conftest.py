import os
from typing import Iterator

import boto3
import pytest
from moto import mock_dynamodb2, mock_s3
{%- if cookiecutter.with_dynamodb_table == "y" %}
from mypy_boto3_dynamodb.service_resource import Table
{%- endif %}
{%- if cookiecutter.with_s3_bucket == "y" %}
from mypy_boto3_s3.service_resource import Bucket
{%- endif %}

from {{ cookiecutter.package_name }} import di


@pytest.fixture(autouse=True)
def environment_variables() -> None:
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
{%- if cookiecutter.with_dynamodb_table == "y" %}
    os.environ["SERVICE_TABLE_NAME"] = "test_service_table"
{%- endif %}
{%- if cookiecutter.with_s3_bucket == "y" %}
    os.environ["SERVICE_BUCKET_NAME"] = "test_service_bucket"
{%- endif %}


{%- if cookiecutter.with_dynamodb_table == "y" %}
@pytest.fixture
def service_table(environment_variables) -> Iterator[Table]:
    with mock_dynamodb2():
        table_name = os.environ["SERVICE_TABLE_NAME"]
        dynamodb = boto3.client("dynamodb")
        dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield boto3.resource("dynamodb").Table(table_name)
{%- endif %}


{%- if cookiecutter.with_s3_bucket == "y" %}
@pytest.fixture
def service_bucket(environment_variables) -> Iterator[Bucket]:
    with mock_s3():
        bucket_name = os.environ["SERVICE_BUCKET_NAME"]
        s3 = boto3.client("s3")
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )
        yield boto3.resource("s3").Bucket(bucket_name)
{%- endif %}


@pytest.fixture(autouse=True)
def clear_di_cache():
    di.clear()
