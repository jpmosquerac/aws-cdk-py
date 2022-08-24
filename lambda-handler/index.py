from __future__ import print_function

import boto3
import json

print('Loading function')

def handler(event, context):
    '''Provide an event that contains the following keys:

      - operation: one of the operations in the operations dict below
      - tableName: required for operations that interact with DynamoDB
      - payload: a parameter to pass to the operation being performed
    '''
    try:
        
        print("Received event: " + json.dumps(event, indent=2))

        body = json.loads(event['body'])

        operation = body['operation']

        if 'tableName' in body:
            dynamo = boto3.resource('dynamodb').Table(body['tableName'])

        operations = {
            'create': lambda x: dynamo.put_item(**x),
            'read': lambda x: dynamo.get_item(**x),
            'update': lambda x: dynamo.update_item(**x),
            'delete': lambda x: dynamo.delete_item(**x),
            'list': lambda x: dynamo.scan(**x),
            'echo': lambda x: x,
            'ping': lambda x: 'pong'
        }

        if operation in operations:
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(operations[operation](body.get('payload')))
            }
        else:
            raise ValueError('Unrecognized operation "{}"'.format(operation))

    except ValueError:
        return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(Exception.__str__)
        }

    except:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Unexpected unexpected error occurred while procesing your request"
        }