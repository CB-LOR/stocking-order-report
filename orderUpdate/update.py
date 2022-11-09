import boto3
import json
import traceback
from datetime import datetime
from decimal import Decimal

ddb = boto3.resource('dynamodb')
table = ddb.Table('stocking-orders')


def lambda_handler(event, context):
    status_update = parse_event(event)
    
    # Add update ts
    add_order_timestamp(status_update)

    # Get all data from table
    order_item = table.update_item(
        Key={
            'email': status_update['email'],
            'order_ts': status_update['order_ts']
        },
        UpdateExpression='set order_ts=:ts, orderStatus=:os',
        ExpressionAttributeValues={
            ':ts': status_update['order_update_ts'],
            ':os': status_update['orderStatus']
        },
        ReturnValues="UPDATED_NEW"
    )

    print(order_item)
 
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(order_item['Attributes'], cls=DecimalEncoder),
    }


class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


def add_order_timestamp(order):
    order['order_update_ts'] = str(datetime.now())


def parse_event(event):
    # check incoming values and create order
    try:
        body = json.loads(event['body'])
        return {
            'email': body['email'],
            'order_ts': body['order_ts'],
            'orderStatus': body['orderStatus']
        }
    except Exception as e:
        print('Failed to get all required attributes', e)
        print(traceback.format_exc())
        return None