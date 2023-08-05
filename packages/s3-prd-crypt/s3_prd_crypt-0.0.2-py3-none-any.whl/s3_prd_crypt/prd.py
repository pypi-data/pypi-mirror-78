# -*- coding: utf-8 -*-
import pandas as pd

from s3_prd_crypt.s3_connector import AWSS3BucketConnector
from s3_prd_crypt.file_type import to_file, from_file


def s3_put_df(
        s3_access_key: str,
        s3_access_secret_key: str,
        bucket_name: str,
        obj_path: str,
        df: pd.DataFrame,
        file_type: str = "parquet",
        encrypt: bool = False,
        key: bytes = None,
        endpoint: str = None):

    """Store DataFrame in S3 bucket.

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:              str, path to store data in bucket
    :param df:                    pd.DataFrame, data to put in S3
    :param file_type:             str, file type to store DataFrame as, default = 'parquet'
                                  Supported file types are 'parquet' and 'csv':

                                  'parquet': DataFrame is stored as parquet file with pandas.DataFrame.to_parquet() with
                                  default parameters and pyarrow engine.
                                  
                                  'csv': DataFrame is stored as csv file with pandas.DataFrame.to_csv() with parameter
                                  index=False.

    :param encrypt:               bool, optional, whether data should be encrypted, default=False

                                  Data are encrypted with the encryption algorithm AES-256 and AWS SSE-C, server-side
                                  encryption with customer-provided encryption keys. This means that the data are
                                  encrypted before storage with a key provided by the user (you).
                                  The user is responsible for not losing the key as it is needed for decrypting the data.
                                  (https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)

    :param key:                   bytes, key to encrypt with if encrypt = True, default = None

    :param endpoint:              str, optional, endpoint, should, if given, be a https endpoint to ensure that the key
                                  and data are sent securely before encryption and storage, default = None
    """

    s3_connector = AWSS3BucketConnector(access_key=s3_access_key,
                                        secret_key=s3_access_secret_key,
                                        bucket_name=bucket_name,
                                        host=endpoint)
    
    data = to_file(df, file_type)

    if encrypt:
        s3_connector.put_encrypt_sse_c(data=data,
                                       obj_name=obj_path,
                                       key=key)
    else:
        s3_connector.put(data=data,
                         obj_name=obj_path)

    return f"{obj_path} successfully stored in bucket {bucket_name}"


def s3_read_df(
        s3_access_key: str,
        s3_access_secret_key: str,
        bucket_name: str,
        obj_path: str,
        file_type: str = None,
        encrypted: bool = False,
        key: bytes = None,
        endpoint: str = None,) -> pd.DataFrame:

    """Read DataFrame stored as parquet or csv from S3 bucket.

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:              str, path to read data from bucket
    :param file_type:             str, file type of stored DataFrame, default = None
                                  Supported file types are 'parquet' and 'csv':

                                  'parquet': Read DataFrame stored as parquet file with pandas.DataFrame.to_parquet()
                                  with default parameters and pyarrow engine.

                                  'csv': Read DataFrame stored as csv file with pandas.DataFrame.to_csv() with parameter
                                  index=False.

    :param encrypted:             bool, optional, whether data should be decrypted, default=False

                                  If data are encrypted, the data will only be decrypted if it was encrypted with
                                  AWS SSE-C, server-side encryption with customer-provided encryption keys, and the key
                                  that was used for encryption.
                                  (https://docs.aws.amazon.com/AmazonS3/latest/dev/ServerSideEncryptionCustomerKeys.html)

    :param key:                   bytes, key to decrypt with if encrypted = True, default = None

    :param endpoint:              str, endpoint, should, if given, be a https endpoint to ensure that the key and data
                                  are sent securely, default = None

    :return data:                 pd.DataFrame, data read from S3 bucket"""

    s3_connector = AWSS3BucketConnector(access_key=s3_access_key,
                                        secret_key=s3_access_secret_key,
                                        bucket_name=bucket_name,
                                        host=endpoint)

    if encrypted:
        res = s3_connector.read_decrypt_sse_c(obj_name=obj_path,
                                              key=key)
    else:
        res = s3_connector.read(obj_name=obj_path)

    df = from_file(res, file_type)
    
    return df


def s3_delete_object(s3_access_key: str,
                     s3_access_secret_key: str,
                     bucket_name: str,
                     obj_path: str,
                     endpoint: str = None):

    """Delete stored object in S3 bucket

    :param s3_access_key:         str, S3 access key
    :param s3_access_secret_key:  str, S3 secret access key
    :param bucket_name:           str, S3 bucket name
    :param obj_path:              str, path of object to delete
    :param endpoint:              str, endpoint, should, if given, be a https endpoint, so that data are sent securely,
                                  default = None
    """

    s3_connector = AWSS3BucketConnector(access_key=s3_access_key,
                                        secret_key=s3_access_secret_key,
                                        bucket_name=bucket_name,
                                        host=endpoint)

    s3_connector.delete(obj_name=obj_path)
