FROM python:3.8.5-slim
LABEL maintainer="MrKoopaKiller <github.com/MrKoopaKiller>"

WORKDIR /usr/src/app

COPY main.py ./
CMD [ "python", "./main.py" ]
