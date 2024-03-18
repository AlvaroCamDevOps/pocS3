import os
import boto3
import mimetypes


def upload_to_s3(local_directory, bucket_name, robot_image, uid, aws_access_key_id, aws_secret_access_key):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # sts_client = boto3.client(
    # 'sts',
    # aws_access_key_id=aws_access_key_id,
    # aws_secret_access_key=aws_secret_access_key
    # )
    # response = sts_client.get_session_token()
    # security_token = response['Credentials']['SessionToken']

    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(robot_image, uid, relative_path).replace("\\", "/")
            content_type = 'application/zip' if file.endswith(".zip") else mimetypes.guess_type(local_path)[0] or 'application/octet-stream'
            s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ContentType': content_type, 'ACL': 'public-read'})
            print(f"Archivo '{local_path}' subido a '{s3_path}'")
    
            url = s3.generate_presigned_url(
                'get_object',
                 Params={'Bucket': access_point_arn, 'Key': s3_path, 'ResponseContentDisposition': 'inline'},
                 ExpiresIn=1800
             )
            print(f"URL del archivo subido: {url}")

if __name__ == "__main__":
    aws_access_key_id = '1'
    aws_secret_access_key = '2'
    bucket_name = '3'
    access_point = '4'
    access_point_arn = '5'
    # access_point_arn = '6'
    local_directory = 'final_report' 
    robot_image = 'robottest'  
    uid = 'test9'  

    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=f'{robot_image}/{uid}/')

    upload_to_s3(local_directory, bucket_name, robot_image, uid, aws_access_key_id, aws_secret_access_key)
