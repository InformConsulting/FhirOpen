import requests
import json

#FHIR_URL = 'http://fhirtest.uhn.ca/baseDstu2/Patient'
FHIR_URL = 'https://argonaut.aidbox.io/fhir/Patient'


def list():
    r = requests.get(FHIR_URL, dict(_format='json', _pretty=True))
    return r.json()


def read(pk):
    r = requests.get('{}/{}'.format(FHIR_URL, pk), dict(_format='json', _pretty=True))
    return r.json()


def create():
    data = {
        "resourceType": "Patient",
        "name": [
            {
                "family": [
                    "Fletchers"
                ],
                "given": [
                    "Arturo",
                    "F"
                ]
            }
        ],
        "gender": "unknown",
        "birthDate": "1942-01-28",
        "deceasedBoolean": False
    }

    r = requests.post(FHIR_URL, json.dumps(data))
    r.headers = {'Accept': 'application/json+fhir', "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    return r.json()


def delete(pk):
    r = requests.delete('{}/{}'.format(FHIR_URL, pk))
    r.headers = {'Accept': 'application/json+fhir'}

    return r


#print(create())
#print(delete('5fb02143-cc23-4eb2-a07d-4f68c745840d'))
print(read('5fb02143-cc23-4eb2-a07d-4f68c745840d'))
