FROM python:3.8-alpine

LABEL maintainer="samedamci@disroot.org"

ENV TOKEN TOKEN
ENV INSTANCE_URL INSTANCE_URL

COPY requirements.txt /requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers libc-dev libffi-dev libressl-dev && \
	pip install -r requirements.txt && \
	mkdir /opt/bot &&\
	printf "%s\n%s" $TOKEN $INSTANCE_URL > /opt/bot/environment && \
	apk del gcc musl-dev linux-headers libc-dev libressl-dev

COPY . /opt/bot/

RUN cd /opt/bot && \
	rm -rf README.md LICENSE requirements.txt .git*

CMD cd /opt/bot/ && python3 main.py
