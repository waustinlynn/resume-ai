import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

from app.infrastructure.persistence.abstract_resume_persistence import (
    AbstractResumePersistence,
    ResumePersistence,
)
from app.infrastructure.settings import Settings

settings = Settings()


GLOBAL_DYNAMODB_CLIENT: DynamoDBServiceResource = None


def get_dynamo_db_client() -> DynamoDBServiceResource:  # type: ignore
    return boto3.resource(
        "dynamodb",
        region_name="us-west-2",
        endpoint_url=settings.db_host,
        aws_access_key_id="fakeAccessKeyId",  # Dummy access key
        aws_secret_access_key="fakeSecretAccessKey",
    )
    # global GLOBAL_DYNAMODB_CLIENT
    # if not GLOBAL_DYNAMODB_CLIENT:
    #     GLOBAL_DYNAMODB_CLIENT =
    #     GLOBAL_DYNAMODB_CLIENT
    # return GLOBAL_DYNAMODB_CLIENT


def get_resume_table_name() -> Table:  # type: ignore
    return get_dynamo_db_client().Table(settings.resume_table_name)


def get_abstract_resume_persistence() -> AbstractResumePersistence:  # type: ignore
    return ResumePersistence(get_resume_table_name())
