from json import loads, dumps

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

config = loads(open('../config.json').read())["forms"]

SCOPES = config["links"]["scope_meta"]
DISCOVERY_DOC = config["links"]["discovery"]
form_id = config["form_id"]

store = file.Storage('../input/token.json')
flow = client.flow_from_clientsecrets('../input/credentials.json', SCOPES)
creds = tools.run_flow(flow, store)

service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

result = service.forms().get(formId=form_id).execute()

with open("../output/meta.bin", "w") as meta:
    meta.write(dumps(result, indent=4))
