import json
import logging

import boto3
from botocore.exceptions import ClientError

from .common_constants import SECRETS_MANAGER_ENDPOINT_URL, AWS_REGION_DEFAULT

logger = logging.getLogger()


def get_ssm_parameters(param_store_path):
    client = boto3.client("ssm")
    parameters = list()
    next_token = ' '
    while next_token is not None:
        ssm_params = client.get_parameters_by_path(
            Path=param_store_path,
            WithDecryption=True,
            NextToken=next_token
        )
        next_token = ssm_params.get("NextToken", None)
        parameters.extend(ssm_params["Parameters"])
    config = [(p["Name"][p["Name"].rfind("/") + 1:], p["Value"]) for p in parameters]
    return dict(config)


def get_secrets(secret_name, env="dev", json_parse=False):
    """
    Params:
        secret_name: Name of the secret
        json_parse: Set to True only if target secret is key/value pair format
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        endpoint_url=SECRETS_MANAGER_ENDPOINT_URL[env],
        region_name=AWS_REGION_DEFAULT
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.exception("Unable to fetch secret from secret manager")
        raise e
    else:
        if json_parse:
            secrets = json.loads(get_secret_value_response['SecretString'])
        else:
            secrets = get_secret_value_response['SecretString']
        return secrets

