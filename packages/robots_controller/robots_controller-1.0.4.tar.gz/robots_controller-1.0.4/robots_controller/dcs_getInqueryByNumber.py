# генерация тестового VB.NET конфига на основе excel Config.xlsx
import pyodbc
import json
import requests
import logging

import abc

def convert_json(obj):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr)
                else:
                    #print(v)
                    v = "{0}".format(v).replace("\"","\"\"").replace('\n'," ").replace('\t'," ").replace('\r'," ")
                    #print(v)
                    str = "out_TransactionItem.SpecificContent("+ f"\"{k}\") = \"{v}\""
                    arr.append(str)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr)
        return arr

    results = extract(obj, arr)
    return results


class error_handler:

    def __init__(self, own_function):
        self.func = own_function

    def __call__(self, *args, **kwargs):
        try:
            self.func(*args, **kwargs)
        except Exception as e:
            print(e)



class ServiceProxyConnector:
    URL = "http://0001ofsbill01.msk.mts.ru:8001/"

    def __init__(self):
        driver  = 'DRIVER={SQL SERVER}'
        server = 'SERVER=0000uipathdb01.msk.mts.ru'
        port = 'PORT=1433'
        database = 'DATABASE=UiPath'
        user = 'Trusted_Connection=yes'
        connStr = ';'.join([driver,server,port,database,user])


        self.conn = pyodbc.connect(connStr)
        self.cursor = self.conn.cursor()

        self.__token = None

    def __del__(self):
        self.conn.close()

    @property
    def token(self):
        if self.__token:
            return self.__token
        else:
            self.__token = self.__login()
            return self.__token

    @error_handler
    def __login(self):
        token = None
        method = "api/users/login"
        params = {"user":{"username": "sgsafono","password": "Q3/eaifc"}}

        reply = requests.post("{0}{1}".format(self.__class__.URL, method), json = params)
        if reply.status_code == 200:
            __json = reply.json()
            token = __json['token']

        return token

    @error_handler
    def getInqueryByNumber(self, srid):
        data = None
        method = "api/incoming/siebel"
        head = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla', 'authorization': 'Token {}'.format(self.token)}
        params = {
        "jsonrpc": "2.0", 
        "method": "getInquiryByNumber", 
        "params": 
        {
            "sender": "test",
            "inquiryNumber": srid,
            "data":"Full"
            
        },
        "id": 1
        }
        reply = requests.post("{0}{1}".format(self.__class__.URL, method), json = params, headers = head)
        if reply.status_code == 200:
            __json = reply.json()
            data = __json["result"]["data"]

        return data  

    @error_handler
    def getInquiryList(self, _dateFrom, _dateTo, _theme, _type, _subTheme, _offlineQueue):
        data = None
        method = "api/incoming/siebel"

        head = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla', 'authorization': 'Token {}'.format(self.token)}

        params = {
                "jsonrpc": "2.0", "method": "getInquiryList", "params": 
                {
                    "sender": "Robot",
                    "dateFrom": _dateFrom,
                    "dateTo": _dateTo,
                    "query": {
                    "FullSR":"Y",
                    "Theme":_theme,
                    "Type":_type,
                    "SubTheme":_subTheme,
                    "OfflineQueue":_offlineQueue,
                    "interactionStatus":"Open"
                    }
                },
                "id": 1
                }      

        reply = requests.post("{0}{1}".format(self.__class__.URL, method), json = params, headers = head)
        if reply.status_code == 200:
            __json = reply.json()
            data = __json["result"]["data"]

        return data 
