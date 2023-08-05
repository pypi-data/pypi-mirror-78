# UnionStation -- the Data Work
# Copyright 2020 The UnionStation Author. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""UnionStation AWS utility library """

import os
import logging
import tqdm
from typing import Dict, List, Generator, Tuple
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from boto3.s3.transfer import TransferConfig

""" Boto3

boto3 doc:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html # noqa: E501

S3 API:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html # noqa: E501

Notes:
1. list_objects_v2() has max-return limit, default 1,000 of the objects
   in a bucket.

2. Session, Client, Resource
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/index.html#sdk-features # noqa: E501

ToDos:
1. multiprocessing
Ref. 1. http://ls.pwd.io/2013/06/parallel-s3-uploads-using-boto-and-threads-in-python/    # noqa: E501
     2. https://stackoverflow.com/questions/51310604/how-to-use-boto3-client-with-python-multiprocessing  # noqa: E501

boto3 client is not picklable and boto3 is not thread safe. So, working
solution either having a global client object defined, or creatng a
client for each of the thread/process. The first one is not convenient,
the 2nd solution take time for making connection for each of the client,
which is not good for uploading small amouht of files.
"""


class S3Access(object):
    """ UnionStation aws class """

    def __init__(self, profile: str = "", **kwargs):
        """ Initialize AWS S3 access object

        Args:
            profile: (str) aws credential profile
            **kwargs: transfer config args.
                      example args:
                        use_threads=False
                        max_concurrency=10
                        multipart_gb=5*1024**3 (5GB)
        """
        self.S3_BUCKET_BASE = "s3://"
        self.active = False
        try:
            if profile in boto3.session.Session().available_profiles:
                self.session = boto3.session.Session(profile_name=profile)
            else:
                self.session = boto3.session.Session()
            self.client = self.session.client("s3")
            self.s3 = self.session.resource("s3")
            self.paginator = self.client.get_paginator("list_objects")
            self.buckets = [b.name for b in self.s3.buckets.all()]
            self.active = True
        except ProfileNotFound:
            logging.error("Missing AWS Authentication!")
        self.config = TransferConfig(**kwargs)

    def url_to_bnk(self, aws_key: str, isfolder=True) -> Tuple[str, str]:
        """Util for bucket and key info from url
        Example: url_to_bnk("s3://vmoml-stagging") returns
                 ('vmoml-stagging', '')
                 url_to_bnk("s3://vmoml-stagging/Raw") returns
                 ('vmoml-stagging', 'Raw/')
        """
        if "s3://" not in aws_key:
            raise ValueError("Incorrect s3 path!")
        s3_url_list = os.path.relpath(aws_key, "s3://").split("/")
        bucket_name = s3_url_list[0]
        if bucket_name not in self.buckets:
            raise ValueError("Bucket unavailable!")
        if len(s3_url_list) < 2:
            return bucket_name, ""
        task_key = "/".join(s3_url_list[1:])
        if not task_key.endswith("/") and isfolder:
            task_key += "/"
        return bucket_name, task_key

    def ls_dir(
        self, aws_key: str, folders: bool = False, full_key: bool = False
    ) -> List[str]:
        """ List TOP LAYER (due to the use of Delimiter)
            objects under the remote aws key prefix.

            Causion: this method use `list_objects_v2` so it
                     has no pagingate and is limited up to
                     1000 items.

           old name: ls_s3_dir

        Args:
            aws_key: a string to the remote aws directory.
            folders: a boolean. If True only folders are returned.

        Returns:
            A list of items inside aws_key.
            Path to "files" are returned with no trailing /.
            Path to "folders" are returned with trailing /.

        Example:
            ls_dir("s3://vmoml-stagging/Raw") returns
            ['TechCrunchcontinentalUSA.csv', 'aws_hello_world.txt',
             'temp_data/']

            ls_dir("s3://vmoml-stagging/test", folders=True) returns
            ['temp_data/']

            ls_dir("s3://vmoml-stagging/test", full_key=True) returns
            ['s3://vmoml-stagging/test/TechCrunchcontinentalUSA.csv',
             's3://vmoml-stagging/test/aws_hello_world.txt',
             's3://vmoml-stagging/test/temp_data/']

        """
        result = []
        if not self.active:
            return result
        bucket_name, s3_key = self.url_to_bnk(aws_key)
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name, Prefix=s3_key, Delimiter="/"
            )
        except Exception as e:
            raise ValueError(
                "Failed to list objects with error: {}".format(str(e))
            )
        # add files
        if not folders and len(response.get("Contents", [])) > 0:
            for item in response["Contents"]:
                item_key = item["Key"][len(s3_key) :]
                result.append(item_key)
        # add folders
        if len(response.get("CommonPrefixes", [])) > 0:
            for item in response["CommonPrefixes"]:
                item_key = item["Prefix"][len(s3_key) :]
                result.append(item_key)
        # remove ""
        if "" in result:
            result.remove("")
        # add full key path is needed
        if full_key:
            result = [os.path.join(aws_key, r) for r in result]
        return result

    def ls_raw(self, aws_key: str) -> [Dict]:
        """ List objects' information with given aws key.
            Causion: this method use `list_objects_v2` so it
                     has no pagingate and is limited up to
                     1000 items.
            old name: ls_s3_objects

        Args:
            aws_key: a string to the remote aws directory

        Returns:
            A [dict] containing information for all objects
            with the prefix key

        Example:
            ls_raw("s3://vmoml-stagging/test") returns
            {'Key': 'test/',
             'LastModified': datetime.datetime(
                 2020, 8, 26, 12, 18, 50, tzinfo=tzutc()),
             'ETag': '"d41d8cd98f00b204e9800998ecf8427e"',
             'Size': 0,
             'StorageClass': 'STANDARD'}
            {'Key': 'test/TechCrunchcontinentalUSA.csv',
             'LastModified': datetime.datetime(
                 2020, 8, 26, 14, 26, 38, tzinfo=tzutc()),
             'ETag': '"426af48e888003ce0fded94b5fa3b093"',
             'Size': 93536,
             'StorageClass': 'STANDARD'}
        """
        if not self.active:
            return []
        bucket_name, s3_key = self.url_to_bnk(aws_key)
        try:
            contents = self.client.list_objects_v2(
                Bucket=bucket_name, Prefix=s3_key
            )["Contents"]
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return contents

    def download(self, aws_key: str, local: str):
        """Download S3 direcotry to local. This method shall behave
           similarly to `sync_down` but with tqdm process bar
           old name: download_dir

        Args:
            aws_key: aws key place to start downloading
            local: local path to folder

        Example:
            download_dir = "/Users/haiyu/H-AI/datalet/temp_data"
            s3.download("s3://vmoml-stagging/Raw", download_dir)
        """
        if not self.active:
            return
        keys = []
        dirs = []
        next_token = ""
        bucket, s3_key = self.url_to_bnk(aws_key)
        base_kwargs = {
            "Bucket": bucket,
            "Prefix": s3_key,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != "":
                kwargs.update({"ContinuationToken": next_token})
            results = self.client.list_objects_v2(**kwargs)
            contents = results.get("Contents")
            for i in contents:
                k = i.get("Key")
                if k[-1] != "/":
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get("NextContinuationToken")

        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
        for k in tqdm.tqdm(keys):
            dest_pathname = os.path.join(local, k)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            self.client.download_file(bucket, k, dest_pathname)

    def gen_objects(
        self,
        aws_key: str,
        suffix: str = "",
        key_only: bool = True,
        full_key: bool = False,
    ) -> Generator:
        """ Generator for iterate objects in a S3 bucket key place.
           old name: get_s3_objects

        Args:
            aws_key: aws key place to start downloading
            suffix: pattern to match in s3 key
            key_only: if True, only yield ['Key'], otherwise yield
                      object contents
            full_key: if True, yield key with full s3 url path

        Returns:
            a generator

        Example:
            s3_obj_gen = s3.gen_objects("s3://vmoml-stagging/Raw", ".jpg")
            for s in s3_obj_gen:
                print(s)

            Case I: gen_objects("s3://vmoml-stagging/Raw", suffix='.jpg', full_key=True) # noqa: E501
            > s3://vmoml-stagging/Raw/Raw/Downtown/FRONT/testrecord_Main_0020.jpg        # noqa: E501

            Case II: gen_objects("s3://vmoml-stagging/Raw", suffix='.jpg', full_key=False) # noqa: E501
            > Raw/Downtown/FRONT/testrecord_Main_0020.jpg

            Case III: gen_objects("s3://vmoml-stagging/Raw", key_only=False)
            > Each of the generator object is a dict like:
                {'Key': 'Raw/Downtown/FRONT/testrecord_Main_0240.jpg',
                'LastModified': datetime.datetime(
                    2020, 7, 6, 2, 39, 23, tzinfo=tzutc()),
                'ETag': '"2ebd77723e00a89b0931732634283cdf"',
                'Size': 244836,
                'StorageClass': 'STANDARD'}
        """
        if not self.active:
            return None
        bucket, prefix = self.url_to_bnk(aws_key)
        kwargs = {"Bucket": bucket, "Prefix": prefix}
        while True:
            resp = self.client.list_objects_v2(**kwargs)
            try:
                contents = resp["Contents"]
            except KeyError:
                return

            for obj in contents:
                key = obj["Key"]
                if (
                    key.startswith(prefix)
                    and key.endswith(suffix)
                    and not key.endswith("/")
                ):
                    if not key_only:
                        yield obj
                    if full_key:
                        yield os.path.join(aws_key, key)
                    else:
                        yield key

            try:
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            except KeyError:
                break

    def gen_keys(
        self,
        aws_key: str,
        suffix: str = "",
        key_only: bool = True,
        full_key: bool = False,
    ) -> Generator:
        """ Generate the keys in an S3 bucket.
            This method works the same as the `get_objects` but
            implemented with paginator.
            The paginator works slightly slower my `get_objects` method.
        """
        if not self.active:
            return None
        bucket, prefix = self.url_to_bnk(aws_key)
        kwargs = {"Bucket": bucket, "Prefix": prefix}
        page_iterator = self.paginator.paginate(**kwargs)
        for page in page_iterator:
            for obj in page["Contents"]:
                key = obj["Key"]
                if (
                    key.startswith(prefix)
                    and key.endswith(suffix)
                    and not key.endswith("/")
                ):
                    if not key_only:
                        yield obj
                    if full_key:
                        yield os.path.join(aws_key, key)
                    else:
                        yield key

    def put(self, bucket: str, local_file: str, object_name: str) -> bool:
        """Upload a file to an S3 bucket
           old_name: upload_file

        Args:
            bucket: Name of the S3 bucket
            local_file: local file to upload
            object_name: S3 object name

        Returns:
            upload status
        """
        if not (self.active and os.path.exists(local_file)):
            return False
        try:
            self.client.upload_file(
                local_file, bucket, object_name, Config=self.config
            )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def up(self, bucket: str, local_file: str, object_name: str) -> bool:
        """Upload a file to an S3 bucket using s3 resource

        Args:
            bucket: Name of the S3 bucket
            local_file: local file to upload
            object_name: S3 object name

        Returns:
            upload status

        Example:
        up("vmoml-stagging", "temp_data/hello_aws.txt", "test/hello_aws.txt")
        """
        if not (self.active and os.path.exists(local_file)):
            return False
        self.s3.Bucket(bucket).upload_file(local_file, object_name)
        return True

    def get(self, bucket: str, object_name: str, local_file: str) -> bool:
        """Download a file from an S3 bucket
           old name: download_file

        Args:
            bucket: Name of the S3 bucket
            object_name: S3 object name
            local_file: local file to save download as

        Returns:
            download status
        """
        if not self.active:
            return False
        try:
            self.client.download_file(
                bucket, object_name, local_file, Config=self.config
            )
        except ClientError as e:
            logging.error(e)
            return False
        return True

    @staticmethod
    def ls_local_objects(local_folder: str) -> [str]:
        """ List recursively file objects under specified local folder

        Args:
            local_folder: folder on local disk

        Returns:
            relative file pathnames.

        Example:
            /tmp
                - example
                    - file_1.txt
                    - some_folder
                        - file_2.txt
            ls_local_objects("/tmp/example")
            ['file_1.txt', 'some_folder/file_2.txt']
        """
        path = Path(local_folder)
        paths = []
        for file_path in path.rglob("*"):
            if file_path.is_dir():
                continue
            str_file_path = str(file_path)
            str_file_path = str_file_path.replace(f"{str(path)}/", "")
            paths.append(str_file_path)
        return paths

    def sync_up(self, local: str, aws_key: str):
        """Sync local to aws_key
           old name sync_from_local

        Args:
            local: folder on local disk
            aws_key: destination s3 prefix
        """
        if not self.active:
            return
        bucket_name, s3_key = self.url_to_bnk(aws_key)
        files = self.ls_local_objects(local_folder=local)
        for f in files:
            target_key = os.path.join(s3_key, f)
            local_file = os.path.join(local, f)
            self.put(bucket_name, local_file, target_key)

    def sync_down(self, aws_key: str, local: str):
        """Sync aws_key to local
           old name: sync_to_local

        Args:
            aws_key: source s3 prefix
            local: destination folder on local disk

        Example:
            sync_down(local="temp_data", aws_key="s3://vmoml-stagging/test")
        """
        if not self.active:
            return
        bucket_name, s3_key = self.url_to_bnk(aws_key)
        object_keys = self.gen_objects(aws_key)
        for ok in object_keys:
            obj = ok[len(s3_key) :]
            dst_folder = os.path.join(local, os.path.dirname(obj))
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            dst_file = os.path.join(local, obj)
            if not os.path.isfile(dst_file):
                self.get(bucket_name, ok, dst_file)

    def _check_key(self, bucket: str, key: str) -> bool:
        if not self.active:
            return False
        try:
            self.s3.Object(bucket, key).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logging.error("Soruce key does not exist!")
                return False
            else:
                raise
        else:
            return True

    def copy(self, src_key: str, dst_key: str):
        """
        example:
        copy(
            src_key="s3://vmoml-stagging/test/hello_aws.txt",
            dst_key="s3://vmoml-stagging/test/temp_data/hello_aws.txt",
        )
        """
        src_bucket, src_key = self.url_to_bnk(src_key, isfolder=False)
        if self._check_key(src_bucket, src_key):
            dst_bucket, dst_key = self.url_to_bnk(dst_key, isfolder=False)
            copy_source = {"Bucket": src_bucket, "Key": src_key}
            self.s3.meta.client.copy(copy_source, dst_bucket, dst_key)

    def rm(self, aws_key: str):
        """
        example:
        rm("s3://vmoml-stagging/test/temp_data/hello_aws.txt")
        """
        bucket, key = self.url_to_bnk(aws_key, isfolder=False)
        if self._check_key(bucket, key):
            self.s3.Object(bucket, key).delete()

    def mv(self, src_key: str, dst_key: str):
        """
        example:
        mv(
            src_key="s3://vmoml-stagging/test/hello_aws.txt",
            dst_key="s3://vmoml-stagging/test/temp_data/hello_aws.txt",
        )
        """
        self.copy(src_key, dst_key)
        self.rm(src_key)
