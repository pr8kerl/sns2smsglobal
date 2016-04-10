# sns2smsglobal

An AWS Lambda function to send an SMS message using [SMS Global](https://www.smsglobal.com/apis/).
The function is configured as a subscription destination for an AWS SNS topic.
Send a message to the topic and you should then receive the message as an SMS to your phone.

The python smsglobal code gratefully stolen from [here](https://github.com/smsglobal/example-python-rest-client).

## Usage

You will need an AWS account of course.
You will need an SMS Global API token and secret available from within your SMS Global dashboard.
You will also need an AWS KMS key as described [here](http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html)

* encrypt the SMS Global secret
Encrypt your SMS global secret and save the resulting Cipher blob.

```
aws kms encrypt --key-id alias/<KMS key name> --plaintext "<SMS Global secret>"
```

* create an iam role
Edit the example policy.json file. Change the key arm to the arn of your KMS key created above.
Then upload the policy.

```
aws iam create-role --role-name sns2smsglobal --assume-role-policy-document file://./role.json
```

* update the configuration file
Edit the file config.ini.
Replace all the values between the angle brackets with your own values. Do not leave the angle brackets there. Do not enclose values within quotes.
The phone number should be in international format without a '+' at the start, just numbers.
The sms origin name is a logical name you can set to identify the source of the sms message. It has to be alphanumeric and between 4 and 11 characters.

```
[sns2smsglobal]
kms_key_alias: <kms key alias name>
smsglobal_key_id: >sms global api key>
smsglobal_secret_blob: <kms encrypted cipher blob of your smsglobal secret>
sms_destination_number: <mobile phone number>
sms_origin_name: <origin name>
```

* create a zip file bundle for Lambda service
Within this source directory and after all changes to the config, create a zip file.

```
zip -r /tmp/sns2smsglobal.zip *
```

* create a lambda function using the zip file

```
aws lambda create-function --function-name sns2smsglobal \
        --runtime python2.7 \
        --role <role arn as per above> \
        --handler lambda_function.lambda_handler \
        --zip-file /tmp/sns2smsglobal.zip \
        --timeout 10 \
        --publish
```

* finally subscribe the lambda function to an existing SNS topic

