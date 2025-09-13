import boto3
from django.conf import settings
from celery import shared_task
import gc

@shared_task(ignore_result=True)
def upload_to_liara(file_content, filename, folder="profile", model_type=None, object_id=None):
    import boto3
    from django.conf import settings
    from io import BytesIO
    import gc

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
        file_obj = BytesIO(file_content)
        s3.upload_fileobj(
            Fileobj=file_obj,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs={'ACL': 'public-read'}
        )

        if model_type == "profile":
            from accounts.models import Profile
            Profile.objects.filter(pk=object_id).update(image_url=public_url)

        elif model_type == "product":
            from shop.models import ProductModel
            ProductModel.objects.filter(pk=object_id).update(image_url=public_url)

        elif model_type == "product_image":
            from shop.models import ProductImageModel
            ProductImageModel.objects.filter(pk=object_id).update(url=public_url)

        print(f"✅ Async Liara upload successful: {public_url}")

    except Exception as e:
        print(f"❌ Async Liara upload failed: {e}")

    finally:
        gc.collect()
          

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
