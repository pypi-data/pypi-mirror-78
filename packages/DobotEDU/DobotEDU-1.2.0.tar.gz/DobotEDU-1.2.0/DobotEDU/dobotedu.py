from DobotRPC import MagicianApi, LiteApi, MagicBoxApi, loggers
from .function import Util, Face, Speech, Nlp, Ocr, Robot, Tmt
import requests
import json

loggers.set_use_file(False)


class DobotEDU(object):
    def __init__(self,
                 user_name: str = None,
                 school_key: str = None):
        if user_name is not None and school_key is not None:
            address = f"http://49.235.112.128:8052/{user_name}/{school_key}"
            json_result = eval(requests.get(address).content.decode())
            API_KEY = f"{json_result[0]}"
            SECRET_KEY = f"{json_result[1]}"
            api_key = API_KEY
            user_data = f"{json_result[2]}"
            account = user_data.split(',', 1)

            self.__host = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=\
client_credentials&client_id={api_key}&client_secret={SECRET_KEY}"

        else:
            self.__host = None
            self.__token = None

        self.__magician_api = MagicianApi()
        self.__lite_api = LiteApi()
        self.__magicbox_api = MagicBoxApi()
        url = "https://dobotlab.dev.ganguomob.com/api/auth/login"
        headers = {"Content-Type": "application/json"}
        payload = {"account": account[0], "password": account[1]}
        r = requests.post(url, headers=headers, data=json.dumps(payload))
        token = json.loads(r.content.decode())["data"]["token"]
        self.__token = token
        self.__face = Face(self.__token)
        self.__ocr = Ocr(self.__token)
        self.__nlp = Nlp(self.__token)
        self.__speech = Speech(self.__token)
        self.__robot = Robot(self.__token)
        self.__tmt = Tmt(self.__token)
        self.__util = Util()

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token: str):
        self.__token = token

        self.__face.token = token
        self.__ocr.token = token
        self.__nlp.token = token
        self.__speech.token = token
        self.__robot.token = token
        self.__tmt.token = token

    @property
    def face(self):
        return self.__face

    @property
    def ocr(self):
        return self.__ocr

    @property
    def nlp(self):
        return self.__nlp

    @property
    def speech(self):
        return self.__speech

    @property
    def robot(self):
        return self.__robot

    @property
    def tmt(self):
        return self.__tmt

    @property
    def util(self):
        return self.__util

    # @property
    # def log(self):
    #     return loggers

    @property
    def magician(self):
        return self.__magician_api

    @property
    def m_lite(self):
        return self.__lite_api

    @property
    def magicbox(self):
        return self.__magicbox_api

    def set_token(self, token):
        self.__token = "Bearer " + token
        self.__ocr = Ocr(self.__token)
        self.__nlp = Nlp(self.__token)
        self.__speech = Speech(self.__token)

    def conversation_robot(self, query, session_id):
        assert self.__host is not None
        """智能对话"""
        response = requests.get(self.__host)
        access_token = response.json()["access_token"]
        url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + str(
            access_token)
        # 下面的log_id在真实应用中要自己生成，可是递增的数字
        log_id = "7758521"
        # 下面的user_id在真实应用中要是自己业务中的真实用户id、设备号、ip地址等，方便在日志分析中分析定位问题
        user_id = "222333"
        # 下面要替换成自己的s_id,是你的机器人ID
        s_id = "S29652"
        post_data = "{\"log_id\":\"" + log_id + "\",\"version\":\"2.0\",\"service_id\":\
        \"" + s_id + "\",\"session_id\":\"" + session_id + "\",\"request\":\
        {\"query\":\"" + query + "\",\"user_id\":\"" + user_id + "\"},\"dialog_state\":\
        {\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1027488\",\"1027844\",\
        \"1027543\",\"1027486\",\"1028485\"]}}}"

        headers = {"Content-Type": "application/json"}
        r = requests.post(url, data=post_data.encode("utf-8"), headers=headers)
        ret = r.json()
        return ret
