from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

server = Flask(__name__)

dynamodb2 = boto3.resource('dynamodb', region_name='us-east-1')
usersTable = dynamodb2.Table('eas-tabla')


@server.route("/", methods=['POST'])
def insertar():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    if 'id' not in data:
        return jsonify({"error": "El campo 'id' es obligatorio"}), 400

    try:
        usersTable.put_item(Item=data)
    except NoCredentialsError:
        return jsonify({"error": "El servidor no tiene credenciales de AWS"}), 503
    except (BotoCoreError, ClientError):
        return jsonify({"error": "No se pudo insertar en DynamoDB"}), 503

    return jsonify({"mensaje": "Registro insertado correctamente", "item": data}), 201


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5001)
