FROM python:3.8.2-slim
WORKDIR /app
COPY ./dist/ ./dist
COPY requirements.txt requirements.txt
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip config set install.trusted-host mirrors.aliyun.com
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install dist/traceint-1.3.6-py3-none-any.whl
