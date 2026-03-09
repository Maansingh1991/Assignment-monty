import boto3
from config.config import AWS_ENDPOINT, DYNAMO_DB_TABLE
from services.s3_upload_service import generate_download_url,delete_image

dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT)
table = dynamodb.Table(DYNAMO_DB_TABLE)


def save_metadata(item):
    table.put_item(Item=item)


def get_metadata(key, id):
    res = table.getItem(Key={[key]: id})
    return res.get("Item")


def delete_metadata(key, id):
    table.delete_item(Key={[key]: id})


def list_images(tag=None, user_id=None, limit=10, last_key=None):
    params = {
        "IndexName": "tag-index",
        "KeyConditionExpression": "tag = :tag",
        "ExpressionAttributeValues": {
            ":tag": tag
        },
        "Limit": limit
    }

    if user_id:
        params["FilterExpression"] = "user_id = :user"
        params["ExpressionAttributeValues"][":user"] = user_id

    if last_key:
        params["ExclusiveStartKey"] = last_key

    response = table.query(**params)

    return {
        "items": response.get("Items", []),
        "nextKey": response.get("LastEvaluatedKey")
    }


def get_image(image_id):
    response = table.get_item(
        Key={
            "image_id": image_id
        }
    )

    item = response.get("Item")

    if not item:
        return {"error": "Image not found"}

    url = generate_download_url(item["s3_key"])

    item["download_url"] = url

    return item


def delete_image(image_id):
    response = table.get_item(
        Key={
            "image_id": image_id
        }
    )

    item = response.get("Item")

    if not item:
        return {"message": "Image not found"}

    s3_key = item["s3_key"]

    delete_image(s3_key)

    table.delete_item(
        Key={
            "image_id": image_id
        }
    )

    return {"message": "Image deleted successfully"}
