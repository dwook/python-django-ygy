from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static/"
    file_overwrite = False  # 같은 이름의 파일이 들어왔을 때 덮어쓰기 X


class UploadStorage(S3Boto3Storage):
    location = "uploads/"
