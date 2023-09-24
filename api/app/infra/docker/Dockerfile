FROM python:3.11-slim
RUN mkdir -p /opt/thriviti
WORKDIR /opt/thriviti
COPY app/src/  ./
ADD app/infra/docker/requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8090
ENTRYPOINT ["uvicorn", "service.service_time_tracking:app", "--host", "0.0.0.0", "--port", "8090"]

