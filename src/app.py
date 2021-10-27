import boto3
import json
import traceback
from decimal import Decimal

ddb = boto3.resource('dynamodb')
table = ddb.Table('stocking-orders')


def lambda_handler(event, context):

    # Get all data from table
    orders = table.scan(
        Select='ALL_ATTRIBUTES'
    )
 
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(orders['Items'], cls=DecimalEncoder),
    }

class DecimalEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(obj)
    return json.JSONEncoder.default(self, obj)

