# coding:utf-8

"""
Author ：daben_chen
封装TAPD Bugs列表

"""

from datetime import date
import json
import requests
from requests.auth import HTTPBasicAuth

# 请求类型对应url
request_type_url = {
    "bugs": "https://api.tapd.cn/bugs" # bugs
}


def request_api_result(user, password, url, parms):
    req = requests.get(url, params=parms, auth=HTTPBasicAuth(user, password))
    data = json.loads(req.content.decode('utf8'))
    return data



class TAPD(object):

    """
    Api doc: https://www.tapd.cn/help/view#1120003271001003101
    """
    
    def __init__(self, user, password):
        self.user = user
        self.password = password

    
    def get_bugs_data(self, data_type, workspace_id, status=None,
                      owner=None, start_date=None, end_date=None):

        """
        :param data_type: 获取bugs
        :param workspace_id: bug项目id
        :return: dict
        """

        if not isinstance(data_type, str):
            raise TypeError("request_type must be string.")        
        if not isinstance(workspace_id, int):
            raise TypeError("workspace_id must be int.")

        parms = {"workspace_id": workspace_id, "limit": 200}

        
        if status:
            if not isinstance(status, str):
                raise TypeError("status must be string.")
            parms["status"] = status

        if owner:
            if not isinstance(owner, str):
                raise TypeError("owner must be str.")
            parms["owner"] = owner

        if start_date and end_date:
            if not isinstance(start_date, date):
                raise TypeError("start_date must be date.")
            if not isinstance(end_date, date):
                raise TypeError("end_date must be date.")
            parms["created"] = str(start_date) + "~" + str(end_date)

        try:
            req_url = request_type_url[data_type]
        except KeyError:
            raise ValueError("request_type must be " + ' or '.join(request_type_url.keys()))
        data = request_api_result(self.user, self.password, req_url, parms)
        return data

def get_target_value(self, key, dic, tmp_list):

    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):
        return "argv[1] not an dict or argv[-1] not an list"

    if key in dic.keys():
        tmp_list.append(dic[key])
        
    for value in dic.values():
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)
        elif isinstance(value, (list, tuple)):
            _get_value(key, value, tmp_list)

    return tmp_list



def _get_value(self, key, val, tmp_list):

    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)
            
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)

"""
例子
"""
# if __name__ == '__main__':
#     test_dic = {'a': '1', 
#                 'b': '2', 
#                 'c': {'d': [{'e': [{'f': [{'v': [{'g': '6'}, [{'g': '7'}, [{'g': 8}]]]}, 'm']}]}, 'h', {'g': [10, 12]}]}}
#     test_list = [1, 2, 3]
#     print("a的值为:", TAPD.get_target_value("a", test_dic, []))
#     print("d的值为:", TAPD.get_target_value("d", test_dic, []))
#     print("g的值为:", TAPD.get_target_value("g", test_dic, []))
#     print("test 的值为:", TAPD.get_target_value("a", "test", []))
#     print("test 的值为:", TAPD.get_target_value("a", test_dic, "test"))
#     print("test 的值为:", TAPD.get_target_value("a", test_dic, test_list))