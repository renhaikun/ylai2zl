#!/bin/bash
PROJECT=ylai2zl
#build项目镜像
cd /data/$PROJECT
docker build -t $PROJECT .
#停止该项目正在运行的容器

echo "停止正在运行的容器ID:  `docker ps -a |grep $PROJECT |grep Up |awk {'print $1'}`"
docker rm -f `docker ps -a |grep '8869\|$PROJECT' |awk {'print $1'}`
sleep 30s

#启动最新build后的容器
docker run -d -p 8869:8088 --gpus '"device=3"' -v /data/ylai2zl:/usr/src/app  -v /daypop-data/video2zl:/usr/src/app/video $PROJECT
sleep 30s
echo "新的$PROJECT容器成功启动,ID:  `docker ps -a |grep $PROJECT |grep Up |awk {'print $1'}`"













