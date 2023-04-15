from json import load


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
        raise IOError(f"Expected dict, got {type(result)}")


def get_response(identifier: str, path: str = "./data/responses.json") -> dict:
    with open(path, 'r') as reader:
        result = load(reader)
        if isinstance(result, dict):
            for response in result["responses"]:
                if response["responseId"] == identifier:
                    return response
            raise IOError(f"Response with id {identifier} not found")
        raise IOError(f"Expected dict, got {type(result)}")


def get_response_by_count(count: int, path: str = "./data/responses.json") -> dict:
    with open(path, 'r') as reader:
        result = load(reader)
        if isinstance(result, dict):
            for response in result["responses"]:
                if response["count"] == count:
                    return response
            raise IOError(f"Response with count {count} not found")
        raise IOError(f"Expected dict, got {type(result)}")


def get_latest_response(path: str = "./data/responses.json") -> dict:
    with open(path, 'r') as reader:
        result = load(reader)
        if isinstance(result, dict):
            for response in result["responses"]:
                if response["count"] == read_number("./counter") - 1:
                    return response
            raise IOError(f"Expected dict, got {type(result)}")
