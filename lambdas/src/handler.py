import json
import os
import boto3
from pydantic import BaseModel, Field, EmailStr, validator

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class Candidato(BaseModel):
    email: EmailStr
    password: str
    name: str
    last_name: str

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("El password debe tener al menos 8 caracteres")
        return password

def main(event, context):
    try:
        # Validar el cuerpo de la petición
        body = json.loads(event['body'])
        candidato = Candidato(**body)

        # Validar que el email no esté registrado
        response = table.get_item(Key={'email': candidato.email})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'El email ya está registrado'})
            }

        # Guardar en DynamoDB
        table.put_item(Item=candidato.dict())

        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'Candidato registrado exitosamente'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
