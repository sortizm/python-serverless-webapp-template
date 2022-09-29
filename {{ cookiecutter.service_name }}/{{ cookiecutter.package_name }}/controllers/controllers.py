import json

from logging import Logger

from aws_lambda_powertools.event_handler.api_gateway import Response
from aws_lambda_powertools.event_handler.exceptions import NotFoundError

from {{ cookiecutter.package_name }} import app, di


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
    logger: Logger = di[Logger]
    logger.info(metadata)
    if isinstance(ex, NotFoundError):
        logger.error(
            f"Not found: {app.current_event.http_method} - {app.current_event.path}"
        )
        return Response(
            status_code=404,
            content_type="application/json+hal",
            body=None,
        )
    else:
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
