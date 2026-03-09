import pytest
from flask import Flask
from routes.uploading_service import uploading_service_blueprint
from unittest.mock import patch
import io


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(uploading_service_blueprint)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_upload_image(client):
    with patch("services.image_service.upload_image") as mock_upload:
        mock_upload.return_value = {
            "image_id": "123",
            "tag": "general",
            "user_id": "12312"
        }

        data = {
            "image": (io.BytesIO(b"fake image"), "test.jpg"),
            "user_id": "12312",
            "tag": "general"
        }

        response = client.post(
            "/image/upload",
            data=data,
            content_type="multipart/form-data"
        )

        assert response.status_code == 200
        assert response.json["image_id"] == "123"

def test_delete_image(client):

    with patch("services.dynamodv_service.delete_image") as mock_delete:

        mock_delete.return_value = {"message": "deleted"}

        response = client.delete("/image/123")

        assert response.status_code == 200
        assert response.json["message"] == "deleted"

from unittest.mock import patch


def test_list_images(client):

    with patch("services.dynamodv_service.list_images") as mock_list:

        mock_list.return_value = {
            "items": [{"image_id": "1"}],
            "nextKey": None
        }

        response = client.get("/image/list?tag=general")

        assert response.status_code == 200
        assert len(response.json["items"]) == 1

from unittest.mock import patch


def test_get_image(client):

    with patch("services.dynamodv_service.get_image") as mock_get:

        mock_get.return_value = {
            "image_id": "123",
            "download_url": "http://example.com/image.jpg"
        }

        response = client.get("/image/123")

        assert response.status_code == 200
        assert response.json["image_id"] == "123"