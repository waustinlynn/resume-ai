from app.infrastructure.settings import Settings

settings = Settings()

RESUME_TABLE_SPEC = {
    "TableName": settings.resume_table_name,
    "KeySchema": [
        {"AttributeName": "id", "KeyType": "HASH"},
        {"AttributeName": "document_type", "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": "id", "AttributeType": "S"},
        {"AttributeName": "document_type", "AttributeType": "S"},
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
}
