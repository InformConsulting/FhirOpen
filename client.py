import requests

url = 'http://fhirtest.uhn.ca/baseDstu2/Patient'
r = requests.get(url, dict(_format='json', _pretty=True))

print(r.json())