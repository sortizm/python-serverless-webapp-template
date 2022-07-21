from test.utils import is_valid_openapi_response, route_request


def test_hello_response_is_valid_according_to_schema() -> None:
    # when
    hello_response = route_request("/hello", "get")

    # then
    is_valid_response = is_valid_openapi_response(
        "/hello", "get", None, hello_response
    )
    assert is_valid_response