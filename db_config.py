#conding=utf-8
#author rhk
#YUE_LI
import pymongo
from pymongo import MongoClient
import urllib.parse
class mongo_cls ():
    def __init__(self):
        self.testdbms = "mongo_replicaset"
        self.testhost1 = "10.129.12.20"
        self.testport1 = 8635
        self.testhost2 = "10.129.12.21"
        self.testport2 = 8635
        self.testuser = "yueli_arabic"
        self.testpassword = "func_arabic_search_cZUlgM1Hqqyn4"
        self.testdatabase = "arabic_search"
        self.testcharset = "utf8"




        self.USER_PRO = ""
        self.PASSWORD_PRO = ""
        self.HOST_PRO = ""

        self.USER_BENDI = ""
        self.PASSWORD_BENDI = ""
        self.HOST_BENDI = "127.0.0.1:27017"
    def mogo_cl(self,env):
        if env == "test":
           client = MongoClient(
                "mongodb://{user}:{password}@{host1}:{port1},{host2}:{port2}/{database}".format(user=self.testuser,
                                                                                                password=urllib.parse.quote_plus(
                                                                                                    self.testpassword),
                                                                                                host1=self.testhost1,
                                                                                                port1=self.testport1,
                                                                                                host2=self.testhost2,
                                                                                                port2=self.testport2,
                                                                                                database=self.testdatabase))["arabic_search"]["video2zl"]
           return client

        elif env == "product":
            client = MongoClient(self.USER_PRO + urllib.parse.quote_plus(self.PASSWORD_PRO) + self.HOST_PRO)
            return client
        else:
            assert  env == "bendi"
            client = MongoClient(self.USER_BENDI + urllib.parse.quote_plus(self.PASSWORD_BENDI) + self.HOST_BENDI)["kg_db"]["video"]
            return client


if __name__ == '__main__':
    import time

    db_simple = {
        "filename": "测试.mp4",  # 文件名
        "filetype": "video/mp4",  # 文件类型
        "lang": "zh",  # 语言
        "status": [0, 0, 0],  # 处理默认初始状态，对应三个，视频处理状态，翻译处理状态，语音识别处理状态，-1为处理失败，0为未处理，1为处理成功
        "viedo_result": {"video": [], "audio_person": [], "audio_scenes": [], "keyframe": []},
        # video处理结果，字典结构，key分别对应切分后的视频文件名，分离后的人声文件名，分离后的背景声文件名，以及关键帧的文件名
        "audio_result": "",  # 语音识别结果
        "nmt_result": "",  # 机器翻译后的结果
        "keywords": "",  # 视频关键词，label
        "db_time": int(time.time()),  # 数据初始入库时间   时间戳
        "completion_time": ""  # 数据完成更新后的时间  时间戳
    }
    m = mongo_cls()
    cl = m.mogo_cl("bendi")
    db= cl.insert_one(db_simple)