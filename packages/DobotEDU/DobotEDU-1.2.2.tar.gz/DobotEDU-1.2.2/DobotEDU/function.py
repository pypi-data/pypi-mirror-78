# -*- coding: utf-8 -*-
import requests
import json
import base64
import sounddevice as sd
import cv2
import uuid


class Util(object):
    def get_image(self,
                  file_path,
                  timeout,
                  port,
                  flip=False):  # timeout为拍照时间,port相机端口，flip是否水平翻转标志
        cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)  # 用摄像头拍照
        t = timeout * 1000
        cnt = timeout + 1
        while True:
            ret, frame = cap.read()  # 读取摄像头拍照的图片
            if flip:
                frame = cv2.flip(frame, 1)  # 左右翻转摄像头获取的照片
            pic = frame.copy()
            dst = cv2.putText(frame, str(cnt), (300, 300),
                              cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4,
                              4)
            cv2.imshow("video", dst)  # 显示照片
            c = cv2.waitKey(1)  # 显示的帧数
            if c == 27:
                break
            if t == 0:
                cv2.imwrite(file_path, pic)
                return
            if t % 1000 == 0:
                cnt = cnt - 1
            t = t - 40

    def record(self, timeout):
        voice_data = sd.rec(int(timeout * 16000), samplerate=16000, channels=1)
        sd.wait()
        return voice_data


class BaseAI(object):
    def __init__(self, token=None):
        self._token = token
        self._url = "https://dobotlab.dev.ganguomob.com/api/ai/tencent-transmit"

    @property
    def _headers(self):
        assert self._token is not None
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
        }

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    def _format(self, data):
        d = json.loads(data.content.decode())['data']
        f_data = json.loads(d)
        return f_data


class Tiia(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def sort(self, image):
        payload = {"data": "{\"ImageBase64\":\"" + image + "\"}", "type": 1}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res


class Face(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def match(self, image_a, image_b):
        payload = {
            "data":
            "{\"ImageA\":\"" + image_a + "\", \"ImageB\":\"" + image_b + "\"}",
            "type": 2
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)["Score"]
        return res

    def detect(self, image, face_attributes=0, quality_detection=0):
        payload = {
            "data":
            "{\"Image\":\"" + image + "\", \"NeedFaceAttributes\":" +
            str(face_attributes) + ",\"NeedQualityDetection\":" +
            str(quality_detection) + "}",
            "type":
            3
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res

    def search(self, group_ids, image):
        payload = {
            "data": "{\"GroupIds\":" + str(group_ids) + ", \"Image\":\"" +
            image + "\"}",
            "type": 4
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res

    def create_library(self, group_name, group_id):
        payload = {
            "data":
            "{\"GroupName\":\"" + group_name + "\", \"GroupId\":\"" +
            group_id + "\"}",
            "type":
            5
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res

    def create_person(self, group_id, person_name, person_id, image):
        payload = {
            "data":
            "{\"GroupId\":\"" + group_id + "\", \"PersonName\":\"" +
            person_name + "\", \"PersonId\":\"" + person_id +
            "\",  \"Image\":\"" + image + "\"}",
            "type":
            7
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res

    def person_info(self, person_id):
        payload = {"data": "{\"PersonId\":\"" + person_id + "\"}", "type": 14}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res

    def delete_library(self, group_id):
        payload = {"data": "{\"GroupId\":\"" + group_id + "\"}", "type": 6}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        return res


class Speech(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def asr(self, voice):
        payload = {
            "data":
            "{\"ProjectId\":1,\"SubServiceType\":2,\"EngSerViceType\":\"16k\",\"SourceType\":\
            1,\"Voice_format\":\"wav\",\"UsrAudioKey\":\"erwe\",\"Data\": \"" +
            voice + "\",\"DataLen\":1500}",
            "type":
            9
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        asr_data = self._format(r)["Result"]
        return asr_data

    def synthesis(self, text, language):
        u = str(uuid.uuid4())
        payload = {
            "data":
            "{\"Text\":\"" + text + "\",\"SessionId\":\"" + u +
            "\",\"ModelType\":1, \"PrimaryLanguage\": " + language + "}",
            "type":
            10
        }
        r = requests.post(self.url,
                          headers=self.headers,
                          data=json.dumps(payload))
        res = self._format(r)['Audio']
        voice_data = base64.b64decode(res)
        return voice_data


class Ocr(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def basic_general(self, image):
        payload = {"data": "{\"ImageBase64\":\"" + image + "\"}", "type": 8}
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        res = self._format(r)
        ocr_data = ""
        for i in range(len(res["TextDetections"][0])):
            ocr_data = ocr_data + res["TextDetections"][i][
                'DetectedText'] + "\n"
        return ocr_data


class Nlp(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def topic(self, text):
        payload = {
            "data": "{\"Text\":\"" + text + "\",\"Flag\":2}",
            "type": 11
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)['Classes'][0]['FirstClassName']
        return data


class Tmt(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def translation(self, source_text, source, target):
        payload = {
            "data":
            "{\"SourceText\":\"" + source_text + "\",\"Source\":\"" + source +
            "\", \"Target\":\"" + target + "\",\"ProjectId\":0 }",
            "type":
            12
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)["TargetText"]
        return data


class Robot(BaseAI):
    def __init__(self, token=None):
        super().__init__(token=token)

    def conversation(self, query, session_id):
        payload = {
            "data":
            "{\"log_id\":\"7758521\",\"version\":\"2.0\",\"service_id\":\"S34433\",\
            \"session_id\":\"\",\"request\":{\"query\":\"你好\",\"user_id\":\"222333\"},\
            \"dialog_state\":{\"contexts\":{\"SYS_REMEMBERED_SKILLS\":[\"1037318\",\
            \"1044905\",\"1044906\",\"1044907\",\"1044908\"]}}}",
            "type": 15
        }
        r = requests.post(self._url,
                          headers=self._headers,
                          data=json.dumps(payload))
        data = self._format(r)
        return data
