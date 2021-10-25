worker_num=1

if [ -n "${WORKER_NUM}" ]; then
    worker_num=${WORKER_NUM}
fi

gunicorn -w ${worker_num} -k uvicorn.workers.UvicornWorker -t 300 -b 0.0.0.0:8088 -e env=test server:app
