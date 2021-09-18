import json
import typing
from http import HTTPStatus

import aiohttp
import logging
from .types import exceptions

TEXTIT_API_URL = "https://textit.ego-ai.tech/api/1.0/data"
log = logging.getLogger("textIT")


def check_result(content_type: str, status_code: int, body: str):
    """
    Checks whether result is a valid API response.
    A result is considered invalid if:
    - The server returned an HTTP response code other than 200
    - The content of the result has content type other than text/html.
    - The method call was unsuccessful (The JSON 'error' field exists)

    :param content_type: content type of result
    :param status_code: status code
    :param body: result body
    :return: The result parsed to a JSON dictionary
    :raises APIError: if one of the above listed cases is applicable
    """
    log.debug('Response: [%d] "%r"', status_code, body)

    if content_type != "text/html":
        raise exceptions.NetworkError(
            f'Invalid response with content type {content_type}: "{body}"'
        )
    try:
        result_json = json.loads(body)
        if isinstance(result_json, list):
            result_json = result_json[0]
    except ValueError:
        result_json = {}

    if isinstance(result_json, dict):
        if error := result_json.get("error"):
            raise exceptions.APIError(f"{error.get('message')} [{error.get('status')}]")

    if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED:
        return result_json
    elif status_code == HTTPStatus.BAD_REQUEST:
        raise exceptions.BadRequest(f"Bad response from API server: {body}")
    elif status_code == HTTPStatus.NOT_FOUND:
        raise exceptions.NotFound(f"Target server not found: {body}")
    elif status_code == HTTPStatus.CONFLICT:
        raise exceptions.Conflict(f"Is there conflict while getting response: {body}")
    elif status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
        raise exceptions.Unauthorized(f"The server did not accept the request: {body}")
    elif status_code >= HTTPStatus.INTERNAL_SERVER_ERROR:
        raise exceptions.APIError(f"Some error while getting response: {body}")
    raise exceptions.APIError(f"{body} [{status_code}]")


async def make_request(
    session: aiohttp.ClientSession, payload: dict
) -> typing.Union[dict, list]:
    log.debug('Make request with payload: "%r"', payload)
    try:
        async with session.post(TEXTIT_API_URL, data=str(payload)) as response:
            return check_result(
                response.content_type, response.status, await response.text()
            )
    except aiohttp.ClientError as e:
        raise exceptions.NetworkError(
            f"aiohttp client throws an error: {e.__class__.__name__}: {e}"
        )
