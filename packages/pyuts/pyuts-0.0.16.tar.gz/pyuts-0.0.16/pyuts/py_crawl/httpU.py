# -*- coding: UTF-8 -*-
from ..py_api_b import PyApiB


class HttpU(PyApiB):
    """
    接口请求
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self,proxy_host=None,proxy_port=None,proxy_user=None,proxy_pswd=None):
        import os
        if proxy_host == None:
            proxy_host = os.getenv('proxy_host','')
        if proxy_port == None:
            proxy_port = os.getenv('proxy_port')
        if proxy_user == None:
            proxy_user = os.getenv('proxy_user')
        if proxy_pswd == None:
            proxy_pswd = os.getenv('proxy_pswd')
        self.proxies = None
        if len(proxy_host) > 0:
            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host" : proxy_host,
                "port" : proxy_port,
                "user" : proxy_user,
                "pass" : proxy_pswd,
            }
            self.proxies = {
                "http"  : proxyMeta,
                "https" : proxyMeta,
            }

    def get(self, url, headers=None, savePath=None):
        import requests
        if savePath == None:
            resp = requests.get(url, proxies=self.proxies, headers=headers)
            return {'code':resp.status_code,'data':resp.text}
        else:
            resp = requests.get(url, proxies=self.proxies, headers=headers, stream=True)
            with open(savePath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
    
        
    def post(self, url, headers=None, dataStr=None, jsonObj=None, savePath=None):
        import requests
        if savePath == None:
            resp = requests.post(url, proxies=self.proxies, headers=headers, data=dataStr, json=jsonObj)
            return {'code':resp.status_code,'data':resp.text}
        else:
            resp = requests.get(url, proxies=self.proxies, headers=headers, stream=True, data=dataStr, json=jsonObj)
            with open(savePath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=512):
                    if chunk:
                        f.write(chunk)
    
    