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
        return str(arg.value)
    elif isinstance(arg, bool):
        return str(arg).lower()
    elif isinstance(arg, int):
        return str(arg)
    return arg


def generate_command(**kwargs) -> typing.Dict:
    """
    Generates dictionary with command for making API request later

    :param kwargs: parameters for generate
    :return: payload
    :rtype: typing.Dict
    """
    command = {}
    for key, value in kwargs.items():
        if not key.startswith("_") and value is not None:
            command[key] = _prepare_arg(value)
    return command


def generate_payload(commands: typing.Union[typing.List, typing.Dict]) -> typing.Dict:
    """
    Generates finished payload for making API request

    :param commands: commands for sending
    :type commands: typing.Union[typing.List, typing.Dict]
    :return: payload
    :rtype: typing.Dict
    """
    if isinstance(commands, dict):
        commands = [commands]
    return {
        "commands": [commands],
        "href": "https://textit.ego-ai.tech/api/1.0/help",
    }


def choose_response(
    responses: typing.List[typing.Dict],
) -> typing.Optional[typing.Dict]:
    """
    Selects the most correct response based on the "probability" field.
    If field is not exists, returns first item.

    :param responses: list of responses to choose from
    :type responses: typing.List[typing.Dict]
    :return: the most correct response
    :rtype: typing.Dict
    """
    if not responses:
        return None
    if all([response.get("probability") for response in responses]):
        responses.sort(key=lambda x: x.get("probability"))
    return responses[0]


def get_func_list(commands: typing.List) -> typing.List[str]:
    """
    Gets only names of commands

    :param commands: list of commands to send
    :type commands: typing.List
    :return: list of names
    :rtype: typing.List[str]
    """
    return [command.get("func") for command in commands]


def sign_responses(func_list: typing.List, responses: typing.List) -> typing.List:
    """
    Signs individual API responses for further identification

    :param func_list: list of command names
    :type func_list: typing.List
    :param responses: list of API responses
    :type responses: typing.List
    :return: list of signed API responses
    :rtype: typing.List
    """
    return [
        {"func": func_name, "response": responses[i]}
        for i, func_name in enumerate(func_list)
    ]
