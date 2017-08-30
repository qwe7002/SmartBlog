FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev uwsgi uwsgi-plugin-python3 python3-pip python3-wheel
RUN pip3 install cffi \
  && pip3 install flask misaka pypinyin pyrss2gen gitpython
WORKDIR /home/SilverBlog
EXPOSE 5000
EXPOSE 5001