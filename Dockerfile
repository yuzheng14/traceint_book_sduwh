FROM python:3.8

RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install flask opencv-python-headless traceint

COPY ./lib_server.py .

CMD python3 lib_server.py
