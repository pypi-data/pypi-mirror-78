FROM python:3.5-alpine

RUN apk add --update --no-cache bash ffmpeg exiftool libffi-dev libmagic
RUN pip install --upgrade pip
RUN apk add --update --no-cache --virtual .build-deps gcc g++ make tzdata ca-certificates python3-dev musl-dev openssl-dev \
  && pip install cryptography python-magic requests termcolor dnspython \
  && pip install pytest pytest-sugar pytest-cov pytest-xdist \
  && apk del .build-deps \
  && rm -rf /root/.cache
