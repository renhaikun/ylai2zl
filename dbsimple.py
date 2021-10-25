#conding=utf-8
#author rhk
#YUE_LI






#默认使用测试数据库，arabic_search
#默认使用表，video2zl

# 视频文件处理说明：
# 1，当前项目路径下的/video文件夹下
# 2，数据处理完成后，请按照当条数据的ID命名创建文件夹，并存放于/video目录下
# 3，处理结果，按照输出类型创建文件夹，并存放数据结果。
# 4，类型说明：video：输出的视频文件，audio_person：输出的人声解说文件，audio_scenes：输出的视频背景音， keyframe：输出的关键帧
# 5，数据ID： 每条数据对应mongodb中的ObjectId
# 视频存储示例说明:
    # 比如传入的数据ID为 5feaed766b96f47bbb0759cc ，那么对应有的目录以及处理结果如下：
    #数据结果文件夹路径：./video/5feaed766b96f47bbb0759cc       此为该条数据处理结果的路径
    #对应的输出视频文件的路径 ：./video/5feaed766b96f47bbb0759cc/video
    #对应的输出的人声解说文件的路径：./video/5feaed766b96f47bbb0759cc/audio_person
    #对应的输出的视频背景音文件的路径：./video/5feaed766b96f47bbb0759cc/audio_scenes
    #对应的输出的关键帧文件的路径：./video/5feaed766b96f47bbb0759cc/keyframe




db_simple = {
    "filename":"", #文件名
    "filetype":"",#文件类型
    "lang":"", #语言
    "status":[0,0,0], #处理默认初始状态，对应三个，视频处理状态，翻译处理状态，语音识别处理状态，-1为处理失败，0为未处理，1为处理成功
    "viedo_result":{"video":[],"audio_person":[],"audio_scenes":[],"keyframe":[]}, #video处理结果，字典结构，key分别对应切分后的视频文件名，分离后的人声文件名，分离后的背景声文件名，以及关键帧的文件名
    "audio_result":"",#语音识别结果
    "nmt_result":"",#机器翻译后的结果
    "keywords":"",#视频关键词，label
    "db_time":"",#数据初始入库时间   时间戳
    "completion_time":""#数据完成更新后的时间  时间戳
}

视频文件上传接口：
http://10.129.15.88:8868/ylai2zl/upload

中英机器翻译接口
http://10.129.15.88:8868/ylai2zl/translation

视频文件处理结果获取接口：
http://10.129.15.88:8868/ylai2zl/download

视频文件标签获取接口：
http://10.129.15.88:8868/ylai2zl/label
