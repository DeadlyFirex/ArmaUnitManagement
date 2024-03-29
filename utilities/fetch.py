from json import loads, dumps
from datetime import datetime

from googleapiclient.errors import HttpError
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

config = loads(open('./config.json').read())

scopes = config["forms"]["links"]["scope"]
discovery_doc = config["forms"]["links"]["discovery"]
form_id = config["forms"]["form_id"]


def __parse_response(response: dict) -> dict:
    result = {
        "responseId": response["responseId"],
        "createTime": response["createTime"],
        "lastSubmittedTime": response["lastSubmittedTime"],
        "count": response["count"],
        "answers": {}
    }
    for answer in response["answers"]:
        result["answers"].update({response["answers"][answer]["questionId"]:
                                  response["answers"][answer]["textAnswers"]["answers"][0]["value"]})
    return result


def run():
    store = file.Storage('./input/token.json')
    creds = store.get()
    refresh_required = False

    # If the credentials are invalid, refresh them
    if creds is None or creds.invalid:
        flow = client.flow_from_clientsecrets('./input/credentials.json', scopes)

        creds = tools.run_flow(flow, store)
        refresh_required = True

    service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=discovery_doc, static_discovery=False)

    try:
        result = service.forms().responses().list(formId=form_id).execute()
    except HttpError as e:
        print(e.__str__())

        flow = client.flow_from_clientsecrets('./input/credentials.json', scopes)
        creds = tools.run_flow(flow, store)
        refresh_required = True

        service = discovery.build('forms', 'v1', http=creds.authorize(
            Http()), discoveryServiceUrl=discovery_doc, static_discovery=False)

        result = service.forms().responses().list(formId=form_id).execute()

    if result is None:
        raise ConnectionError("No response from Google.")

    else:
        with open(config["forms"]["counter"], "w") as dumper:
            dumper.write(str(result["responses"].__len__()))

        datetime_list = dict()
        result_parsed = {"responses": list()}

        for entry in result["responses"]:
            datetime_list.update({entry["responseId"]: datetime.strptime(entry["createTime"], "%Y-%m-%dT%H:%M:%S.%fZ")})
        datetime_list = [i[0] for i in sorted(datetime_list.items(), key=lambda x: x[1])]

        for entry in result["responses"]:
            entry.update({"count": datetime_list.index(entry["responseId"])})
            result_parsed["responses"].append(__parse_response(entry))

        with open("./output/responses.bin", "w") as dumper, open("./data/responses.json", "w") as dumper_2:
            dumper.write(dumps(result, indent=4))
            dumper_2.write(dumps(result_parsed, indent=4))

        return result_parsed, result, result_parsed["responses"].__len__(), refresh_required


def refresh():
    from argparse import Namespace

    store = file.Storage('./input/token.json')
    creds = store.get()

    flags = Namespace(auth_host_name=config["forms"]["refresh_host"],
                      auth_host_port=config["forms"]["refresh_port"],
                      logging_level=config["forms"]["refresh_logging_level"],
                      noauth_local_webserver=config["forms"]["refresh_remote"])

    flow = client.flow_from_clientsecrets('./input/credentials.json', scopes)

    creds = tools.run_flow(flow, store, flags)

    service = discovery.build('forms', 'v1', http=creds.authorize(
        Http()), discoveryServiceUrl=discovery_doc, static_discovery=False)
    return service
