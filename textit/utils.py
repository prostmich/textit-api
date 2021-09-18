import typing
from enum import Enum


def _normalize(obj):
    """
    Normalize dicts and lists

    :param obj: object to normalize
    :return: normalized object
    """
    if isinstance(obj, list):
        return [_normalize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items() if v is not None}
    return obj


def _prepare_arg(arg):
    """
    Stringify arguments

    :param arg: argument for stringify
    :return: prepared argument
    """
    if arg is None:
        return ""
    if isinstance(arg, list):
        return [_prepare_arg(v) for v in arg]
    elif isinstance(arg, dict):
        return {k: _prepare_arg(v) for k, v in arg.items()}
    elif isinstance(arg, Enum):
        return arg.value
    elif isinstance(arg, bool):
        return str(arg).lower()
    return arg


def generate_payload(**kwargs) -> typing.Dict:
    """
    Generates payload for making API request

    :param kwargs: parameters for sending
    :return: payload
    :rtype: typing.Dict
    """
    commands = {}
    for key, value in kwargs.items():
        if not key.startswith("_") and value is not None:
            commands[key] = _prepare_arg(value)
    return {
        "commands": [commands],
        "href": "https://textit.ego-ai.tech/api/1.0/help",
    }


def choose_response(responses: typing.List[typing.Dict]) -> typing.Dict:
    """
    Selects the most correct response based on the "probability" field.
    If field is not exists, returns first item.

    :param responses: list of responses to choose from
    :type responses: typing.List[typing.Dict]
    :return: the most correct response
    :rtype: typing.Dict
    """
    if all([response.get("probability") for response in responses]):
        responses.sort(key=lambda x: x.get("probability"))
    return responses[0]
