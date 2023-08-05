# coding:utf-8

"""
Author ：daben_chen
封装TAPD bug项目

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