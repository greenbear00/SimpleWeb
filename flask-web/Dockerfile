FROM python:3.7

# install vi Editor
RUN apt-get update
RUN apt-get install -y vim

RUN mkdir /tmp/logs

# 가상환경이 아닌 자체에 requirements를 설치해서 실행
WORKDIR /app
ADD . /app
RUN rm -rf venv
RUN pip install -r requirements.txt

RUN sed -i -e 's/\r$/\n/' gunicorn.sh

CMD ["uwsgi", "uwsgi.ini"]
#ENTRYPOINT ["./gunicorn.sh"]