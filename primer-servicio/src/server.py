from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
from boto3.dynamodb.conditions import Key

server = Flask(__name__)

dynamodb2 = boto3.resource('dynamodb', region_name='us-east-1')
usersTable = dynamodb2.Table('eas-tabla')


@server.route("/", methods=['GET'])
def hello():
    user_id = request.args.get('id', '1')

    print("ID recibido:", user_id)

    try:
        response = usersTable.query(
            KeyConditionExpression=Key('id').eq(user_id)
        )
    except NoCredentialsError:
        return jsonify({"error": "El servidor no tiene credenciales de AWS"}), 503
    except (BotoCoreError, ClientError):
        return jsonify({"error": "No se pudo consultar DynamoDB"}), 503

    return jsonify(response)


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)