import requests
import json

FHIR_URL = 'http://fhirtest.uhn.ca/baseDstu2/Patient'


def list():
    r = requests.get(FHIR_URL, dict(_format='json', _pretty=True))
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

print(create())