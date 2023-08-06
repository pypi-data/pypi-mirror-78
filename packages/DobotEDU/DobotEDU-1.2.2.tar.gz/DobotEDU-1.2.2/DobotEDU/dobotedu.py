from DobotRPC import MagicianApi, LiteApi, MagicBoxApi, loggers
from .function import Util, Face, Speech, Nlp, Ocr, Robot, Tmt
import requests
import json

loggers.set_use_file(False)


class DobotEDU(object):
    def __init__(self, account: str = None, password: str = None):
        if account is not None and password is not None:
            try:
                url = "https://dobotlab.dev.ganguomob.com/api/auth/login"
                headers = {"Content-Type": "application/json"}
                payload = {"account": account, "password": password}
                r = requests.post(url,
                                  headers=headers,
                                  data=json.dumps(payload))
                token = json.loads(r.content.decode())["data"]["token"]
            except Exception as e:
                token = None
                loggers.get('DobotEDU').exception(e)
                loggers.get('DobotEDU').error(f"报错原因:服务器出问题啦请联系技术人员:{e}")
        else:
            token = None
            loggers.get('DobotEDU').info("您还未输入用户名和密码,智能API不可以使用哦")

        self.__token = token
        self.__magician_api = MagicianApi()
        self.__lite_api = LiteApi()
        self.__magicbox_api = MagicBoxApi()
        self.__robot = Robot(self.__token)
        self.__face = Face(self.__token)
        self.__ocr = Ocr(self.__token)
        self.__nlp = Nlp(self.__token)
        self.__speech = Speech(self.__token)
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
