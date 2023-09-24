FROM python:3.11-slim
RUN mkdir -p /opt/thriviti
WORKDIR /opt/thriviti
COPY src/  ./
ADD infra/docker/requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD [ "python", "./main.py"]

