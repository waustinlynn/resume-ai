import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
    ResumePersistence,
)
from app.infrastructure.persistence.resume_table_definition import RESUME_TABLE_SPEC
from app.infrastructure.settings import Settings

settings = Settings()


GLOBAL_DYNAMODB_CLIENT: DynamoDBServiceResource = None


def get_dynamo_db_client() -> DynamoDBServiceResource:  # type: ignore
    global GLOBAL_DYNAMODB_CLIENT
    if not GLOBAL_DYNAMODB_CLIENT:
        GLOBAL_DYNAMODB_CLIENT = boto3.resource(
            "dynamodb",
            region_name="us-west-2",
            endpoint_url=settings.db_host,
            aws_access_key_id=settings.db_aws_access_key_id,
            aws_secret_access_key=settings.db_aws_secret_access_key,
        )
    return GLOBAL_DYNAMODB_CLIENT


def get_resume_table() -> Table:  # type: ignore
    client = get_dynamo_db_client()
    # throws ResourceInUseException if table already exists
    try:
        client.create_table(**RESUME_TABLE_SPEC)
    except client.meta.client.exceptions.ResourceInUseException:
        pass

    table = client.Table(settings.resume_table_name)
    table.wait_until_exists()

    return table


def get_abstract_resume_persistence() -> AbstractResumePersistence:  # type: ignore
    return ResumePersistence(get_resume_table())
