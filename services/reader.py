from json import load
from datetime import datetime


def read_number(path: str) -> int:
    """
    Reads a number from a file.
    This requires the first line of the file to be a number.
    Throws an I/O error if the file is empty or the first line is not a number.

    :param path: The path to the file.
    :return: Integer
    """
    with open(path, 'r') as reader:
        try:
            result = int(reader.readline())
        except ValueError as error:
            raise IOError(f"Expected int, got {type(result)}.\nMore info: {error.__str__()}")
        return result


def get_response_ids(path: str = "./data/responses.json") -> list:
    with open(path, 'r') as reader:
        result = load(reader)
        data = []
        if isinstance(result, dict):
            for response in result["responses"]:
                data.append(response["responseId"])
            return data
        else:
            raise IOError(f"Expected dict, got {type(result)}")


def get_response(identifier: str, path: str = "./data/responses.json", parsed: bool = True) -> dict:
    with open(path, 'r') as reader:
        result = load(reader)
        if isinstance(result, dict):
            for response in result["responses"]:
                if response["responseId"] == identifier:
                    if parsed:
                        return _parse_response(response)
                    return response
            raise IOError(f"Response with id {identifier} not found")
        else:
            raise IOError(f"Expected dict, got {type(result)}")


def _parse_response(response: dict) -> dict:
    result = {
        "responseId": response["responseId"],
        "createTime": response["createTime"],
        "lastSubmittedTime": response["lastSubmittedTime"],
        "answers": {}
    }
    for answer in response["answers"]:
        result["answers"].update({response["answers"][answer]["questionId"]:
                                  response["answers"][answer]["textAnswers"]["answers"][0]["value"]})
    return result


def get_latest_response(path: str = "./data/responses.json") -> dict:
    datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    latest_response = None
    latest_datetime = datetime.strptime("1900-01-01T00:10:30.000000Z", datetime_format)

    with open(path, 'r') as reader:
        result = load(reader)
        if isinstance(result, dict):
            for response in result["responses"]:
                current_datetime = datetime.strptime(response["createTime"], datetime_format)
                if current_datetime > latest_datetime:
                    latest_datetime = current_datetime
                    latest_response = response
            return _parse_response(latest_response)
        else:
            raise IOError(f"Expected dict, got {type(result)}")



