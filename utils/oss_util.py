# -*- coding: utf-8 -*-
# @Time    : 2022/10/26 20:02
# @Author  : Destiny_
# @File    : oss_util.py
# @Software: PyCharm

# 上传文件到oss

import oss2
from utils import file_util


class OssMange(object):
    _first = True
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._first:
            return
        config = file_util.arg_yaml()
        self.AccessKeyId = config['AccessKeyId']
        self.AccessKeySecret = config['AccessKeySecret']
        self.EndpointWithoutHTTPS = config['Endpoint']
        self.Endpoint = f"https://{config['Endpoint']}"
        self.Bucket = config['Bucket']

        self.auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
        self.bucket = oss2.Bucket(self.auth, self.Endpoint, self.Bucket)
        # bucket_info = bucket.get_bucket_info()
        self._first = False

    def delete_file(self):
        for obj in oss2.ObjectIterator(self.bucket):
            if obj.is_prefix():
                print('delete directory: ' + obj.key)
            else:
                print('delete file: ' + obj.key)

    def push_object(self, file_dir: str) -> str:
        """
        上传本地文件到oss
        :param file_dir: 本地文件完整目录
        :return: url of object in oss
        """
        root_dir = '/'
        if file_dir.endswith('xls'):
            root_dir = 'excel/'
        if '/' in file_dir:
            oss_file = file_dir.split('/')[-1]
        else:
            oss_file = file_dir
        oss_dir = f'{root_dir}{oss_file}'
        rename_index = 0
        while self.bucket.object_exists(oss_dir):
            oss_file_name = oss_file.split('.')[0]
            oss_file_prefix = oss_file.split('.')[-1]
            if '_' in oss_file:
                oss_file_name = oss_file_name.split('_')[0]
            oss_file = f'{oss_file_name}_{rename_index}.{oss_file_prefix}'
            oss_dir = f'{root_dir}{oss_file}'
            print(f'duplicate name,rename to {oss_dir}')
            rename_index += 1
        self.bucket.put_object_from_file(oss_dir, file_dir)
        return f'https://{self.Bucket}.{self.EndpointWithoutHTTPS}/{oss_dir}'


def oss_push_object(file_dir):
    return OssMange().push_object(file_dir)
