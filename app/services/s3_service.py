import aioboto3
from botocore.config import Config as BotoConfig

from app.core.config import Config
from app.core.logger import logger


class S3Service:
    def __init__(self):
        self.session = aioboto3.Session()

    async def upload_file(
        self, content: str, s3_key: str, content_type: str = "text/plain"
    ) -> str:
        async with self.session.client(
            "s3",
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            endpoint_url=Config.S3_ENDPOINT_URL,
            config=BotoConfig(
                signature_version="s3v4", s3={"addressing_style": "path"}
            ),
        ) as s3:
            try:
                await s3.put_object(
                    Bucket=Config.S3_BUCKET_NAME,
                    Key=s3_key,
                    Body=content,
                    ContentType=content_type,
                )
                return f"s3://{Config.S3_BUCKET_NAME}/{s3_key}"
            except Exception as e:
                logger.error(f"S3 upload error: {str(e)}")
                raise e

    async def get_file(self, s3_key: str) -> str:
        async with self.session.client(
            "s3",
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            endpoint_url=Config.S3_ENDPOINT_URL,
        ) as s3:
            try:
                response = await s3.get_object(Bucket=Config.S3_BUCKET_NAME, Key=s3_key)
                content = await response["Body"].read()
                return content.decode("utf-8")
            except Exception as e:
                logger.error(f"S3 download error: {str(e)}")
                raise e

    async def ping(self) -> bool:
        async with self.session.client(
            "s3",
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            endpoint_url=Config.S3_ENDPOINT_URL,
            config=BotoConfig(
                signature_version="s3v4", s3={"addressing_style": "path"}
            ),
        ) as s3:
            try:
                await s3.head_bucket(Bucket=Config.S3_BUCKET_NAME)
                return True
            except Exception as e:
                logger.error(f"S3 ping error: {str(e)}")
                return False


s3_service = S3Service()
