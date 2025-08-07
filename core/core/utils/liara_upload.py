import boto3
from django.conf import settings

def upload_to_liara(file, filename, folder="profile"):  
    file.seek(0) 
    config = settings.LIARA_OBJECT_STORAGE

    endpoint_url = 'https://storage.c2.liara.space'
    bucket_name = config['bucket_name']
    key = f"{folder}/{filename}"
    public_url = f"https://{bucket_name}.storage.c2.liara.space/{key}"

    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key']
    )
    
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=key,
        ExtraArgs={'ACL': 'public-read'}
    )

    return public_url
