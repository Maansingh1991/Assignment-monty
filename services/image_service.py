import uuid
from services import s3_upload_service,dynamodv_service
import datetime


def upload_image(user_id, filename, data, tag):
    image_id = str(uuid.uuid4())
    key = f"{image_id}_filename"
    s3_upload_service.upload_image_to_s3(key, data)
    metadata = {
        "image_id": image_id,
        "user_id": user_id,
        "filename": filename,
        "tag": tag,
        "uploaded_at":  datetime.date.today().isoformat(),
        "s3_key": key
    }
    dynamodv_service.save_metadata(metadata)
    return metadata


