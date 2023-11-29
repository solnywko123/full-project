FROM python:3

ENV PYTHONENCODING UTF-8
ENV TZ=Asia/Bishkek

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

RUN mkdir static && mkdir media

COPY . .

RUN python3 manage.py collectstatic --noinput







