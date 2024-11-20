# This is a Python script that reads file and write to DocumentReference in FHIR server

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import base64
import json
import requests

defaults = {
    'file-name': 'example.txt',
    'fhir-type-coding': {
        "system": "http://loinc.org",
        "code": "18842-5",
        "display": "Discharge summary"
    },
    'fhir-patient': 'Patient/1',
    'fhir-date': '2022-01-01T00:00:00+00:00',
    'fhir-attachment': {
        "contentType": "text/plain",
        "language": "en-US",
        "data": ""
    },
    'fhir-server': 'http://localhost:8080/fhir/DocumentReference'
}


def read_file(name=defaults.get('file-name')):
    print('Data File: ' + name)
    data = open(name, 'rb').read()
    encoded = base64.b64encode(data)
    encoded_string = encoded.decode('ascii')

    print('Encoded Data File: ' + encoded_string)
    return encoded_string


def write_to_fhir(data):
    with open('documentreference_template.json', 'r') as f:
        json_documentreference = json.load(f)

    json_documentreference["type"]["coding"][0] = defaults.get('fhir-type-coding')
    json_documentreference["subject"]["reference"] = defaults.get('fhir-patient')
    json_documentreference["date"] = defaults.get('fhir-date')
    json_documentreference["content"][0]["attachment"] = defaults.get('fhir-attachment')
    json_documentreference["content"][0]["attachment"]["data"] = data

    print(json.dumps(json_documentreference))

    headers = {'Content-Type': 'application/json+fhir', 'Authorization': 'Basic Y2xpZW50OnNlY3JldA=='}
    r = requests.post(defaults.get("fhir-server"),
                      headers=headers,
                      json=json_documentreference)

    if 201 != r.status_code:
        return [r.status_code, 'writing to fhir server failed']

    return ['201', r.headers]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1:
        encoded_data = read_file(sys.argv[1])
    else:
        encoded_data = read_file()

    print (write_to_fhir(encoded_data))
