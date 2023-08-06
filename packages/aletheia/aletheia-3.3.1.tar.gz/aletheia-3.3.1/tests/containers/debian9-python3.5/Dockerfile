FROM python:3.5-stretch

RUN apt-get update; apt-get install -y ffmpeg libimage-exiftool-perl; apt-get clean
RUN pip install --upgrade pip \
  && pip install pytest pytest-sugar pytest-cov pytest-xdist \
  && pip install cryptography file-magic requests termcolor dnspython \
  && rm -rf /root/.cache
