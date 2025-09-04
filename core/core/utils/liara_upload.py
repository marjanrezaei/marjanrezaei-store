import boto3
from django.conf import settings

def upload_to_liara(file, filename, folder="profile"):
    """
    Upload a Django file to Liara Object Storage and return public URL.
    :param file: Django UploadedFile instance (request.FILES['file'])
    :param filename: Name of the file to store
    :param folder: Folder path in bucket
    :return: Public URL of uploaded file, or None if failed
    """
    if not file:
        return None

    file.seek(0)  # Ensure we read from the beginning

    config = settings.LIARA_OBJECT_STORAGE
    bucket_name = config['bucket_name']
    endpoint_url = "https://storage.c2.liara.space"
    key = f"{folder}/{filename}"
    public_url = f"https://{bucket_name}.storage.c2.liara.space/{key}"

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key']
    )

    try:
        s3.upload_fileobj(
            Fileobj=file,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs={'ACL': 'public-read'}
        )
        print(f"✅ Liara upload successful: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Liara upload failed: {e}")
        return None


def delete_from_liara(key: str):
    """
    Delete a file from Liara Object Storage by key.
    Example key: "products/123_image.jpg"
    """
    config = settings.LIARA_OBJECT_STORAGE
    bucket_name = config['bucket_name']
    endpoint_url = "https://storage.c2.liara.space"

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key']
    )

    try:
        s3.delete_object(Bucket=bucket_name, Key=key)
        print(f"✅ File deleted from Liara: {key}")
    except Exception as e:
        print(f"❌ Delete error ({key}): {e}")
