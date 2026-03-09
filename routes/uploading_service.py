from flask import Blueprint, request, jsonify
from services import image_service, dynamodv_service
import json

uploading_service_blueprint = Blueprint("uploading_service", __name__)


#
# @uploading_service_blueprint.route("/upload/image")
# def get_images():
#     return {"message": "API up and running"}


@uploading_service_blueprint.route("/image/upload", methods=["POST"])
def upload_image():
    file = request.files["image"]
    user_id = request.form["user_id"]
    tag = request.form.get("tag", "general")
    data = file.read()

    result = image_service.upload_image(
        user_id,
        file.filename,
        data,
        tag
    )
    return jsonify(result)


@uploading_service_blueprint.route("/image/list", methods=["GET"])
def list_all_images():
    tag = request.args.get("tag")
    user_id = request.args.get("user_id")
    limit = int(request.args.get("limit", 10))
    last_key = request.args.get("last_key")
    if last_key:
        last_key = json.loads(last_key)
    result = dynamodv_service.list_images(
        tag=tag,
        user_id=user_id,
        limit=limit,
        last_key=last_key
    )

    return jsonify(result)


@uploading_service_blueprint.route("/image/<image_id>", methods=["GET"])
def get_image(image_id):
    result = dynamodv_service.get_image(image_id)

    return jsonify(result)


@uploading_service_blueprint.route("/image/<image_id>", methods=["DELETE"])
def delete_image(image_id):
    result = dynamodv_service.delete_image(image_id)

    return jsonify(result)
