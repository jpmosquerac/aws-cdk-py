import json

def sum(numA, numB):
    try:
        return numA + numB
    except:
        return None


def handler(event, context):
    print(event)

    data = json.loads(event['body'])
    numA = data['numA']
    numB = data['numB']

    result = sum(numA, numB)

    if result!=None:
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('{result}')
        }
    return {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Request Failed!')
    }