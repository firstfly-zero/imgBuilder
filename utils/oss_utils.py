from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError

class Cos():
    def __init__(self, secret_id, secret_key, region):

        self.client = CosS3Client(CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=None, Scheme="https"))

    def upload_file(self, bucket, key, local_path):
        for i in range(0, 10):
            try:
                self.client.upload_file(
                    Bucket=bucket,
                    Key=key,
                    LocalFilePath=local_path
                )
                return key
            except CosClientError or CosServiceError as e:
                print(e)

    def get_url(self, bucket, key):
        return self.client.get_object_url(
            Bucket=bucket,
            Key=key
        )

