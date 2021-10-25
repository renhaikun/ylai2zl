#conding=utf-8
#author rhk
#YUE_LI
from fastapi import FastAPI, Form, Request,UploadFile,File,Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from YUELI.logger import YULI_LOG
from db_config import mongo_cls
from api_config import api_config
from bson import ObjectId
import os
import requests
import uvicorn
import sys
import json
import requests
import time
from bson import ObjectId


modbcls = mongo_cls()

if sys.argv[1] == "test":
    API = api_config.test_config
elif sys.argv[1]  == "product":
    API = api_config.pro_config
elif sys.argv[1]  == "mini" :
    API = api_config.mini_config
else:
    assert sys.argv[1]  == "bendi"
    API = api_config.bendi_config

db = modbcls.mogo_cl(sys.argv[1])
log = YULI_LOG("ylai2zl")
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/ylai2zl/download", StaticFiles(directory="./video"))

@app.post("/ylai2zl/upload")
async def upload(*,file: UploadFile = File(...)):
    # db = modbcls.mogo_cl(os.environ.get("env"))
    #up_data = {"filename": file.filename, "filetype": file.content_type}
    _id = ObjectId()
    meta_type = file.filename.split(".")[-1]
    up_data = dict(
            _id=_id,
            name=file.filename,
            meta_type=meta_type,
            keywords=[],
            keyframe=[],
            origin="movies/{}.{}".format(_id,file.content_type),
            video_clip=[],
            human_audio='',
            bg_audio='',
            sharpness='',
            duration=0,
            status=0,
            create_time=int(time.time()*1000)
        )

    log.info({"msg":"获取视频文件:{}".format(file.filename)})
    # db.close()
    log.info({"msg":"视频存储MongoDB_ID:{}".format(str(_id))})
    data_path = "usr/app/video/movies"
    log.info({"msg": "视频存储路径:{}".format(data_path)})
    if not os.path.exists("data_path"):
         log.info({"msg": "创建视频目录:{}".format(data_path)})
         os.mkdir(data_path)
    log.info({"msg":"读取视频文件:{}".format(data_path)})
    data = await file.read()
    video_name = f'{_id}.{meta_type}'
    # path_video = f'{config.VIDEO_PATH}/{movies}/{_id}.{suffix}'
    with open("{}/{}".format(data_path,video_name),"wb") as f:
        log.info({"msg":"视频文件写入，文件名:{}".format(video_name)})
        f.write(data)
    video_r_data = {"id":str(id),"video_path":"{}/{}".format(data_path,video_name)}
    try:
        log.info({"msg":"请求视频算法接口"})
        statu_video_post = requests.post(API.get("video"),data=video_r_data).status_code
        if statu_video_post == 200:
            log.info({"msg": "请求视频算法接口成功"})
            result = {"code":"1","result_id":str(_id),"msg":"接收video成功，请稍后根据result_id查询相关信息"}
            return result
        else:
            result = {"code":"0","result_id":str(_id),"msg":"接收video成功，请求视频算法服务失败，请联系开发人员反馈"}
            return result
    except:
        log.info({"msg": "请求视频算法接口是失败"})
        result = {"code": "0", "result_id": str(_id), "msg": "接收video成功，算法服务出错，请联系开发人员反馈"}
        return result





@app.post("/ylai2zl/translation")
async def translation(*,text:str = Form(None),id:str = Form(None),lang:str = Form(None),request: Request):
    if text!=None and id ==None:
        log.info({"msg": "执行文本翻译"})
        try:
            translation_data = {"text":text}
            log.info({"msg": "请求翻译接口"})
            translation_result = requests.post(API.get("nmt"),data=translation_data).json()
            log.info({"msg": "翻译成功"})
            result = {"code": "1",  "msg": "获取机器翻译结果成功", "nmt_result":translation_result}
            return result
        except:
            log.info({"msg": "翻译失败"})
            result = {"code": "0",  "msg": "获取机器翻译结果失败，翻译算法出错，请联系开发人员反馈","nmt_result":""}
            return result
    else:
        log.info({"msg": "执行查询视频文本翻译"})
        assert id != None
        # db = modbcls.mogo_cl(os.environ.get("env"))
        log.info({"msg": "链接数据库成功"})
        log.info({"msg": "查询数据ID{}".format(id)})
        try:
            result_db = db.find_one({"_id": ObjectId(id)})
        except:
            log.info({"msg":"翻译数据ID有误，请检查ID是否符合规范"})
            result = {"code": "0", "result_id": str(id), "msg": "机器翻译获取失败，请检查ID输入是否正确", "nmt_result": ""}
            return result
        if result_db:
            if result_db.get("status_all") == 1:
                log.info({"msg": "查询数据成功"})
                result = {"code":"1","result_id":str(id),"msg":"获取机器翻译结果成功","nmt_result":result_db.get("translation_res")}
                return result
            else:
                log.info({"msg": "查询结果，翻译未完成"})
                result = {"code":"0","result_id":str(id),"msg":"暂未获取到机器翻译结果，请稍后查询","nmt_result":""}
                return result
        else:
            result = {"code": "0", "result_id": str(id), "msg": "机器翻译获取失败，请检查ID输入是否正确", "nmt_result": ""}
            return result


@app.post("/ylai2zl/download")
async def download(*,id:str = Form(...)):
    # file_type_list =["video","audio_person","audio_scenes","keyframe","video_all"]
    if id:
        # if file_type in file_type_list:
        try:
            log.info({"msg": "查询文件id : {}".format(id)})
            data_path = "./video/results/{}/video_all.zip".format(str(id))
            if os.path.exists(data_path):
                log.info({"msg": "查询文件成功"})
                with open(data_path, "rb") as f:
                    data = f.read()
                    log.info({"msg": "读取文件成功"})
                return Response(content=data)
            else:
                log.info({"msg": "查询文件结果，未处理完成"})
                result = {"code": "0", "result_id": str(id), "msg": "处理未完成，请稍后获取"}
                return result
        except:
            log.info({"msg": "请求方输入文件类型有误"})
            result = {"code": "0", "result_id": str(id), "msg": "处理失败，请联系开发人员反馈"}
            return result
        # else:
        #     result = {"code": "0", "result_id": str(id), "msg": "当前输入文件类型不存在，请检查需要获取的文件类型"}
        #     return result

@app.post("/ylai2zl/label")
async def label(*,id:str = Form(...)):
    if id:
        log.info({"msg": "开始查label数据ID：{}".format(id)})
        try:
            result_ = db.find_one({"_id": ObjectId(id)})
        except:
            log.info({"msg":"label数据ID有误，请检查ID是否符合规范"})
            result = {"code": "0", "result_id": str(id), "msg": "获取视频标签失败，请检查数据ID"}
            return result
        if result_:
            if result_.get("status_all") == 1 :
                log.info({"msg": "label数据查询成功"})
                lablel_video = result_.get("keywords")
                result = {"code": "1", "result_id": str(id), "msg": "获取视频标签成功",
                          "label": lablel_video}
                return result
            else:
                log.info({"msg": "视频算法处理未完成"})
                result = {"code": "0", "result_id": str(id), "msg": "视频算法处理未完成，请稍后查询"}
                return result
        else:
            result = {"code": "0", "result_id": str(id), "msg": "获取视频标签失败，请检查数据ID"}
            return result

    else:
        log.info({"msg":"请求方未传入ID"})
        result = {"code": "0", "result_id": str(id), "msg": "获取视频标签失败，请检查数据ID",
                  "label": ""}
        return result










if __name__ == '__main__':
    log.info({"msg":"server start"})
    uvicorn.run(app,host = "0.0.0.0",port = 8130)
