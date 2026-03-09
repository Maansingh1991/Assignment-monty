# Image Upload Service (Flask + S3 + DynamoDB + LocalStack)

This project implements a simple **image storage service similar to Instagram**.
It allows users to:

* Upload images
* Store metadata in DynamoDB
* List images with filters and pagination
* Generate a download URL
* Delete images

The project uses:

* **Flask** – REST API framework
* **AWS S3** – image storage
* **DynamoDB** – metadata storage
* **LocalStack** – local AWS emulation
* **Docker Compose** – container orchestration

---

# Architecture

Client
│
Flask API (port 5000)
│
LocalStack (port 4566)
├── S3 (image storage)
└── DynamoDB (metadata storage)


To run the full environment including:

* Flask API
* LocalStack
* S3 bucket
* DynamoDB tables

Run:

```
docker compose up
```

This will automatically:

* Start Flask application
* Start LocalStack
* Create required AWS resources

Resources created automatically:

* **S3 bucket:** `image-bucket`
* **DynamoDB table:** `images`

Flask API will be available at:

```
http://localhost:5000
```

---

# Running Flask Application Manually

If you want to run Flask without Docker:

## Step 1 – Comment Flask service in docker-compose

Disable the **flask-app** service in `docker-compose.yml`.

---

## Step 2 – Update endpoint configuration

Change the LocalStack endpoint in `config.py`:

```
http://localstack:4566
```

to

```
http://localhost:4566
```

---

## Step 3 – Start LocalStack

```
docker compose up localstack
```

---

## Step 4 – Create required AWS resources manually

### Create S3 Bucket

```
aws --endpoint-url=http://localhost:4566 s3 mb s3://image-bucket
```

---

### Create DynamoDB Table

```
aws --endpoint-url=http://localhost:4566 dynamodb create-table \
--table-name images \
--attribute-definitions \
AttributeName=image_id,AttributeType=S \
AttributeName=tag,AttributeType=S \
AttributeName=uploaded_at,AttributeType=S \
--key-schema AttributeName=image_id,KeyType=HASH \
--billing-mode PAY_PER_REQUEST \
--global-secondary-indexes \
IndexName=tag-index,\
KeySchema=[{AttributeName=tag,KeyType=HASH},{AttributeName=uploaded_at,KeyType=RANGE}],\
Projection={ProjectionType=ALL}
```

---

## Step 5 – Run Flask

```
python app.py
```

Application runs at:

```
http://localhost:5000
```

---

# API Endpoints

## Upload Image

POST `/image/upload`

Form Data:

| Field   | Type   | Description    |
| ------- | ------ | -------------- |
| image   | file   | Image file     |
| user_id | string | User ID        |
| tag     | string | Image category |

Example:

```
POST /image/upload
```

---

## List Images

GET `/image/list`

Query Parameters:

| Parameter | Description      |
| --------- | ---------------- |
| tag       | Filter by tag    |
| user_id   | Filter by user   |
| limit     | Pagination limit |
| last_key  | Pagination key   |

Example:

```
GET /image/list?tag=general&limit=5
```

---

## Get Image

GET `/image/{image_id}`

Returns metadata and download URL.

Example:

```
GET /image/878e1cad-a823-4698-98a8-04355c89f313
```

---

## Delete Image

DELETE `/image/{image_id}`

Example:

```
DELETE /image/878e1cad-a823-4698-98a8-04355c89f313
```

---

# Testing

Tests are written using **pytest**.

Run tests:

```
pytest
```

Test coverage includes:

* Upload image
* List images
* Get image
* Delete image

---

# Postman Collection

A Postman collection is provided to test all APIs.

Import the file:

```
image-service-postman-collection.json
```

in Postman.

---

# Requirements

Python dependencies:

```
Flask
boto3
pytest
pytest-mock
```

Install:

```
pip install -r requirements.txt
```


