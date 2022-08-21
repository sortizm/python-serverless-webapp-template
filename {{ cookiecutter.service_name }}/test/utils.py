import json
from typing import Any, Optional, Dict

import yaml
from aws_lambda_powertools.event_handler.api_gateway import Response
from openapi_core import create_spec
from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.response.validators import ResponseValidator

from {{ cookiecutter.package_name }} import get_openapi_schema_location
from {{ cookiecutter.package_name }}.controllers.controllers import handler


def openapi_response_from_api_response(response: Response) -> OpenAPIResponse:
    return OpenAPIResponse(
        data=json.loads(response.body) if response.body else None,
        mimetype=response.headers.get("Content-Type"),
        status_code=response.status_code,
    )


def openapi_schema() -> Any:
    with open(get_openapi_schema_location(), "r") as schema:
        spec_dict = yaml.safe_load(schema)
        return create_spec(spec_dict)


def is_valid_openapi_response(
    request_url: str,
    request_method: str,
    request_body: Optional[str],
    response: Response,
) -> bool:
    schema = openapi_schema()
    validator = ResponseValidator(schema)
    request = OpenAPIRequest(
        full_url_pattern=request_url,
        body=request_body,
        method=request_method.lower(),
        mimetype=None,
    )
    result = validator.validate(request, openapi_response_from_api_response(response))
    if result.errors:
        print(result.errors)
    return result.errors == []


def route_request(
    url: str, method: str = "GET", body: Optional[Dict[str, Any]] = None
) -> Response:
    route, query_string = url.split("?") if "?" in url else (url, "")
    event = {
        "version": "2.0",
        "routeKey": "ANY /{proxy+}",
        "rawPath": route,
        "rawQueryString": query_string,
        "headers": {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "content-length": "0",
        },
        "requestContext": {
            "http": {
                "method": method.upper(),
                "path": route,
                "protocol": "HTTP/1.1",
            },
            "routeKey": "ANY /{proxy+}",
            "stage": "$default",
        },
        "queryStringParameters": {
            qs.split("=")[0]: qs.split("=")[1] for qs in query_string.split("&") if qs
        },
        "pathParameters": {"proxy": str(route).lstrip("/")},
        "isBase64Encoded": False,
    }
    if body:
        event["body"] = json.dumps(body)
    raw_response = handler(event, None)
    return Response(
        status_code=raw_response.get("statusCode"),
        body=raw_response.get("body"),
        content_type=raw_response.get("headers").get("Content-Type"),
        headers=raw_response.get("headers")
    )
