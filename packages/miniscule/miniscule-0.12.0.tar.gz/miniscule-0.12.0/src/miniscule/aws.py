import json
import logging

import yaml

from miniscule.base import ConfigLoader

log = logging.getLogger(__name__)


try:
    import boto3
    import botocore

    IGNORED_EXCEPTIONS = (
        botocore.exceptions.ClientError,
        botocore.exceptions.NoCredentialsError,
    )
except ImportError:
    pass
else:

    def init():
        yaml.add_constructor(
            "!aws/sm", secrets_manager_constructor, Loader=ConfigLoader
        )
        yaml.add_constructor(
            "!aws/secret", secrets_manager_constructor, Loader=ConfigLoader
        )

    def _secrets_manager_client():
        return boto3.client("secretsmanager")

    def secrets_manager_constructor(loader, node):
        friendly_name = loader.construct_yaml_str(node)
        client = _secrets_manager_client()

        secret_string = None
        try:
            response = client.get_secret_value(SecretId=friendly_name)
            secret_string = response.get("SecretString")
        except IGNORED_EXCEPTIONS as exc:
            log.warning(
                "Unable to obtain secrets manager value for %s: %s", friendly_name, exc
            )
            return None
        return _maybe_parse_secret_string(secret_string)

    def _maybe_parse_secret_string(secret_string):
        if secret_string is None:
            return None
        return _maybe_parse_as_json(secret_string) or secret_string

    def _maybe_parse_as_json(secret_string):
        try:
            return json.loads(secret_string)
        except json.JSONDecodeError:
            return None

    init()
