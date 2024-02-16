FROM python:3.10.6

MAINTAINER jiayifei <916457600@qq.com>

# 更新 apt-get 并安装依赖
RUN sed -i 's/http:\/\/deb.debian.org/http:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN sed -i 's/http:\/\/security.debian.org/http:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y ffmpeg

# 设置工作目录
WORKDIR /app
COPY . /app

# 安装依赖
RUN pip3 install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

# 执行器运行
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
