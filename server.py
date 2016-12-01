import json
import os
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.sql import text

CONFIG = os.path.abspath('./server_config.py')

app = Flask(__name__)
app.config.from_pyfile(CONFIG)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
connection = engine.connect()


@app.route('/', methods=['GET'])
def index():
    return 'Sample FHIR server'


@app.route('/fhir/admin/<resource_type>', methods=['POST', 'DELETE'])
def admin(resource_type):
    """
    Метод, для создания и удаления ресурсов.
    Например: 
        POST   http://localhost:5000/fhir/admin/Patient - создаем ресурс Patient
        DELETE http://localhost:5000/fhir/admin/Patient - удаляем ресурс Patient

    DELETE - delete
    POST - create
    """

    if request.method == 'POST':
        raw = 'SELECT fhir_create_storage(\'{"resourceType": "%(type)s"}\');' % {'type': str(resource_type)}
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)

    if request.method == 'DELETE':
        raw = 'SELECT fhir_drop_storage(\'{"resourceType": "%(type)s"}\');' % {'type': str(resource_type)}
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)


@app.route('/fhir/<resource_type>', methods=['GET', 'POST'])
def list(resource_type):
    """
    GET - search
    POST - create
    """

    if request.method == 'GET':
        query_string = request.query_string
        raw = 'SELECT fhir_search(\'{"resourceType": "%(type)s", "queryString": "%(query)s"}\');' % {'type': str(resource_type), 'query': str(query_string)}
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)

    if request.method == 'POST':
        raw = 'SELECT fhir_create_resource(\'{"resource": %s}\');' % json.dumps(request.json)

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
        raw = 'SELECT fhir_read_resource(\'{"resourceType": "%(type)s", "id": "%(pk)s"}\');' % {'type': str(resource_type), 'pk': str(pk)}
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)

    if request.method == 'PUT':
        raw = 'SELECT fhir_update_resource(\'{"resource": %s}\');' % json.dumps(request.json)
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)

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

    if request.method == 'GET':
        raw = 'SELECT fhir_vread_resource(\'{"resourceType": "%(type)s", "id": "%(pk)s", "versionId": "%(vpk)s"}\');' % {'type': str(resource_type), 'pk': str(pk), 'vpk': str(vpk)}
        query = connection.execute(text(raw))
        result = query.fetchone()[0]

        return jsonify(**result)


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
