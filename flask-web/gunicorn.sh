#!/bin/bash


if [ ! -d /tmp/logs ]; then
  mkdir /tmp/logs
fi

FLASK_PID=`ps -aux | grep gunicorn | grep -v grep | awk '{print $2}'`

if [ "${FLASK_PID}" ]; then
  kill $FLASK_PID
  echo "restart ..."
  echo "gunicorn restart..." >> /tmp/logs/flask.log
  sleep 1
else
  echo "start..."
  echo "gunicorn start..." >> /tmp/logs/flask.log
fi

sleep 1

#python3 -m venv venv
#source venv/bin/activate
#pip install --upgrade pip
#ls -l requirements.txt
#pip install -r requirements.txt
#export PYTHONPATH=/opt/SimpleWeb/venv/lib/python3.6/site-packages:$PYTHONPATH



gunicorn --workers 4 --timeout=10 --bind 0.0.0.0:5000 app:app >> /tmp/logs/flask.log
#gunicorn web:app -b 0.0.0.0:5000 -w 2 --timeout=10 -k gevent >> /tmp/logs/flask.log
