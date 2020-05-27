# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import base64
from botocore.exceptions import ClientError

def create_secret():
    secret_name = "secret3"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.create_secret(
            Name=secret_name,
            Description='secret for prod',
            SecretString='real secret to be stored'
        )
    except ClientError as ClientExp:
        print "Client Error: ", ClientExp
    except Exception as exp:
        print "error: ", exp
    else:
    # create secret:  {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '1b137688-2303-4f7d-a6b7-17d7ba447d44', 
    # 'HTTPHeaders': {'date': 'Wed, 27 May 2020 17:18:59 GMT', 'x-amzn-requestid': '1b137688-2303-4f7d-a6b7-17d7ba447d44', 
    # 'content-length': '145', 'content-type': 'application/x-amz-json-1.1', 'connection': 'keep-alive'}}, 
    # u'VersionId': u'a2b8bfac-4dee-47d2-b069-e1d1677518e5', u'Name': u'secret3', 
    # u'ARN': u'arn:aws:secretsmanager:us-east-2:474711206021:secret:secret3-FD5Qis'}
        print "create secret: ", response

def get_secret():

    secret_name = "secret3"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            #raise e
            print "secret not found %s", e
            #raise e
    except Exception as exception:
        print "exception: ", exception 
    else:
        print "get secret: ", get_secret_value_response
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            print "Secret: ", secret, " ARN: ", get_secret_value_response["ARN"]
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            print "decoded_binary_secret: ", decoded_binary_secret



def update_secret():

    secret_name = "secret3"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.update_secret
    # SecretsManager.Client.exceptions.InvalidParameterException
    # SecretsManager.Client.exceptions.InvalidRequestException
    # SecretsManager.Client.exceptions.LimitExceededException
    # SecretsManager.Client.exceptions.EncryptionFailure
    # SecretsManager.Client.exceptions.ResourceExistsException
    # SecretsManager.Client.exceptions.ResourceNotFoundException
    # SecretsManager.Client.exceptions.MalformedPolicyDocumentException
    # SecretsManager.Client.exceptions.InternalServiceError
    # SecretsManager.Client.exceptions.PreconditionNotMetException

    try:
        get_secret_value_response = client.update_secret(
            SecretId=secret_name,
            SecretString="Update2")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            #raise e
            print "secret not found: ", e
            #raise e
    except Exception as exception:
        print "exception: ", exception 
    else:
    # update secret:  {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '5bcd06b1-f3b5-4fd1-b4d8-219e14bec908', 
    # 'HTTPHeaders': {'date': 'Wed, 27 May 2020 17:22:16 GMT', 
    # 'x-amzn-requestid': '5bcd06b1-f3b5-4fd1-b4d8-219e14bec908', 
    # 'content-length': '145', 'content-type': 'application/x-amz-json-1.1', 'connection': 'keep-alive'}}, 
    # u'VersionId': u'86638a4e-3796-4567-90fa-a259760a87a8', u'Name': u'secret3', 
    # u'ARN': u'arn:aws:secretsmanager:us-east-2:474711206021:secret:secret3-FD5Qis'}
        print "update secret: ", get_secret_value_response

    # Your code goes here. 


def delete_secret():

    secret_name = "secret3"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.delete_secret    # SecretsManager.Client.exceptions.InvalidParameterException
    try:
        get_secret_value_response = client.delete_secret(
            SecretId=secret_name,
            ForceDeleteWithoutRecovery=True)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            #raise e
            print "secret not found: ", e
            #raise e
    except Exception as exception:
        print "exception: ", exception 
    else:
        # delete secret:  {'ResponseMetadata': {'RetryAttempts': 0, 'HTTPStatusCode': 200, 'RequestId': '7399de77-be79-441d-9f1d-405aca18fde2', 
        # 'HTTPHeaders': {'date': 'Wed, 27 May 2020 17:33:39 GMT', 'x-amzn-requestid': '7399de77-be79-441d-9f1d-405aca18fde2', 
        # 'content-length': '126', 'content-type': 'application/x-amz-json-1.1', 'connection': 'keep-alive'}}, 
        # u'DeletionDate': datetime.datetime(2020, 5, 27, 13, 33, 39, 481000, tzinfo=tzlocal()), 
        # u'Name': u'secret3', u'ARN': u'arn:aws:secretsmanager:us-east-2:474711206021:secret:secret3-FD5Qis'}
        print "delete secret: ", get_secret_value_response
                
    # Your code goes here.



#create_secret()
#get_secret()
#update_secret()
delete_secret()

# import boto3
# from botocore.exceptions import ClientError
# import json

# def lambda_handler(event, context):
#     #region_name = "us-east-2"
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.list_objects(Bucket="rh-lambda-out-2019")
#     except ClientError as e:
#         return False
#     else:
#         print "response: ", response
#     return True


# lambda_handler(0, 0)
