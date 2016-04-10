from __future__ import print_function

import SMSGlobalAPI
import json
import ConfigParser
import boto3
from base64 import b64decode

kms = boto3.client('kms')
config = ConfigParser.ConfigParser()
config.read('config.ini')
glblkey = config.get('sns2smsglobal', 'smsglobal_key_id')
glblscrtblob = config.get('sns2smsglobal', 'smsglobal_secret_blob')
glblscrt = kms.decrypt(CiphertextBlob = b64decode(glblscrtblob))['Plaintext']
destination = config.get('sns2smsglobal', 'sms_destination_number')
origin = config.get('sns2smsglobal', 'sms_origin_name')

def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    apiWrapper = SMSGlobalAPI.Wrapper(glblkey, glblscrt, "https", "api.smsglobal.com", 443, "v1", "", False, SMSGlobalAPI.Wrapper.TYPE_JSON)
    body = json.dumps({'origin': origin, 'destination': destination, 'message': message})
    response = json.loads(apiWrapper.post("sms",None,body))
    print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))
    return response

