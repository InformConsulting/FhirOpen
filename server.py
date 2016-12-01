import json
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text


app = Flask(__name__)
engine = create_engine('postgresql://postgres:aHTMLPNNdra3pq@localhost/fhirbase')
connection = engine.connect()


@app.route('/', methods=['GET'])
def index():
    return 'Sample FHIR server'


@app.route('/fhir/<resource_type>', methods=['GET', 'POST'])
def list(resource_type):
    """
    POST - create
    """

    raw = 'SELECT fhir_create_resource(\'{"resource": {"resourceType": "%(type)s", "name": [{"given": ["Smith"]}]}}\');' % {'type': str(resource_type)}
    query = connection.execute(text(raw))
    result = query.fetchone()[0]
    return jsonify(**result)


@app.route('/fhir/<resource_type>/<pk>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def read(resource_type, pk):
    """
    GET - read
    PUT - update
    PATCH - patch
    DELETE - delete
    """

    if request.method == 'GET':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'PATCH':
        pass

    if request.method == 'DELETE':
        pass

    return jsonify({})


@app.route('/fhir/<resource_type>/<pk>/_history/<vpk>', methods=['GET'])
def vread(resource_type, pk, vpk):
    """
    GET - vread
    """
    return jsonify({})


@app.route('/fhir/<resource_type>/_search', methods=['POST'])
def search(resource_type):
    """
    POST - search
    """
    return jsonify({})


@app.route('/fhir', methods=['OPTIONS'])
@app.route('/fhir/metadata', methods=['GET'])
def capabilities():
    """
    GET - capabilities
    OPTIONS - capabilities
    """
    return jsonify({})


if __name__ == '__main__':
    app.run(debug=True)