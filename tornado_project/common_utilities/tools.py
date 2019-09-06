import gzip
import json
import uuid


def get_uuid1():
    """ make a UUID based on the host ID and current time
    """
    s = uuid.uuid1()
    return str(s)


def get_gzip(py_data):
    # 压缩成 gzip 数据，python 类型 2 gzip
    json_data = json.dumps(py_data)
    byte_data = bytes(json_data, encoding='utf-8')
    gzip_data = gzip.compress(byte_data)
    return gzip_data


def ungzip(gzip_data):
    # 解压 gzip 数据，gzip 2 python类型
    json_data = gzip.decompress(gzip_data).decode("utf-8")
    py_data = json.loads(json_data)
    return py_data
