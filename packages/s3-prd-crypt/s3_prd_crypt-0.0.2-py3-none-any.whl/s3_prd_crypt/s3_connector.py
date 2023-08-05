# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError, ParamValidationError


class AWSS3BucketConnector:
    """Amazon S3 Storage compatible connection to bucket"""

    def __init__(self, access_key, secret_key, host, bucket_name):

        self.s3 = boto3.resource(
            service_name="s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=host
        )

        try:
            self.s3.meta.client.head_bucket(Bucket=bucket_name)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                raise ValueError(f"Bucket {bucket_name} does not exist")
            else:
                raise PermissionError(f"Was not able to access S3 with given access keys and/or endpoint")
        else:
            self.bucket_name = bucket_name

    def put(self, data, obj_name: str):
        try:
            obj = self.s3.Object(self.bucket_name,
                                 obj_name)
            obj.put(Body=data)
        except (ParamValidationError, ClientError) as err:
            raise ValueError(f"Data storage to bucket {self.bucket_name} failed: {err}")
        else:
            return f"Successfully stored data to bucket {self.bucket_name}"

    def put_encrypt_sse_c(self, data, obj_name: str, key: bytes):
        """Writing and encrypting data with AWS server side encryption and customer-provided encryption key"""
        try:
            obj = self.s3.Object(self.bucket_name,
                                 obj_name)
            obj.put(Body=data,
                    SSECustomerKey=key,
                    SSECustomerAlgorithm="AES256")

        except (ParamValidationError, ClientError) as err:
            raise ValueError(f"Data storage to bucket {self.bucket_name} with encryption failed: {err}")
        else:
            return f"Successfully encrypted and stored data to bucket {self.bucket_name}"

    def read(self, obj_name: str) -> bytes:
        try:
            obj = self.s3.Object(self.bucket_name, obj_name)
            data = obj.get()['Body'].read()
        except (ParamValidationError, ClientError) as err:
            raise ValueError(f"Failed to read data from bucket {self.bucket_name}: {err}")
        else:
            return data

    def read_decrypt_sse_c(self, obj_name: str, key: bytes) -> bytes:
        """Reading and decrypting data with AWS server-side encryption and customer-provided encryption key"""
        try:
            obj = self.s3.Object(self.bucket_name, obj_name)
            data = obj.get(SSECustomerKey=key,
                           SSECustomerAlgorithm="AES256")['Body'].read()
        except (ClientError, ParamValidationError) as err:
            raise ValueError(f"Failed to decrypt and read object from bucket {self.bucket_name}: {err}")
        else:
            return data

    def delete(self, obj_name):
        try:
            obj = self.s3.Object(self.bucket_name, obj_name)
            obj.delete()
        except (ClientError, ParamValidationError) as err:
            raise ValueError(f"Failed to delete data from bucket {self.bucket_name}: {err}")
