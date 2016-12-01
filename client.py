import requests
import json

#FHIR_URL = 'http://fhirtest.uhn.ca/baseDstu2/Patient'
FHIR_URL = 'https://argonaut.aidbox.io/fhir/Patient'
ENCOUNTER_URL = 'https://argonaut.aidbox.io/fhir/Encounter'


def list():
    r = requests.get(FHIR_URL, dict(_format='json', _pretty=True))
    return r.json()


def read(pk, history=None):
    params = dict(_format='json', _pretty=True)
    h = str()

    if history is not None:
        h = '/_history/%s' % history
    print('{}/{}{}'.format(FHIR_URL, pk, h))
    r = requests.get('{}/{}{}'.format(FHIR_URL, pk, h), params)
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


def encounter(pk):
    params = dict(_format='json', _pretty=True, patient=pk)
    r = requests.get('{}/{}'.format(ENCOUNTER_URL, pk), params)
    r.headers = {'Accept': 'application/json+fhir'}
    return r.json()

#print(create())
#print(delete('5fb02143-cc23-4eb2-a07d-4f68c745840d'))
print(read('920fc6eb-b341-46b3-aa1a-e36605729be8', '5584a7e4-8e9f-4f24-b786-a5a896912013'))
