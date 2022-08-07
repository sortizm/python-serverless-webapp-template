import json
import logging

from aws_lambda_powertools.event_handler.api_gateway import Response

from {{ cookiecutter.package_name }} import app


@app.get("/hello")
def hello_world() -> Response:
    return Response(
        status_code=200,
        body=json.dumps({"msg": "hello world", "_links": {"self": {"href": "/hello"}}}),
        content_type="application/json+hal"
    )


@app.exception_handler(Exception)
def handle_exception(ex: Exception):
    metadata = {"path": app.current_event.path}
    logging.info(metadata)
    logging.exception(ex)

    error_response = {
        "error_name": ex.__class__.__name__,
        "error_description": str(ex),
    }

    return Response(
        status_code=500,
        content_type="application/json+hal",
        body=json.dumps(error_response),
    )


def handler(event, context):
    return app.resolve(event, context)
