import os
from logging import Logger
from pathlib import Path
from typing import Dict, Any

import boto3
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
{%- if cookiecutter.with_dynamodb_table == "y" %}
from mypy_boto3_dynamodb.service_resource import Table
{%- endif %}
{%- if cookiecutter.with_s3_bucket == "y" %}
from mypy_boto3_s3.service_resource import Bucket
{%- endif %}


from {{ cookiecutter.package_name }}.logger import init_logger

app = APIGatewayHttpResolver()


def get_openapi_schema_location() -> Path:
    root_directory = Path(__file__).parent
    return root_directory.parent.joinpath("doc", "openapi.yml").resolve()


{%- if cookiecutter.with_dynamodb_table == "y" %}
def get_service_table() -> Table:
    return boto3.resource(
        "dynamodb", region_name=os.getenv("AWS_REGION", "eu-west-1")
    ).Table(os.getenv("SERVICE_TABLE_NAME", ""))
{%- endif %}


{%- if cookiecutter.with_s3_bucket == "y" %}
def get_service_bucket() -> Bucket:
    return boto3.resource("s3").Bucket(os.getenv("SERVICE_BUCKET_NAME", ""))
{%- endif %}


def init_di() -> Dict:
    _logger = init_logger()
    cont: Dict[Any, Any] = {
        Logger: _logger
    }
    return cont


di = init_di()
