FROM pytorch/torchserve:latest-gpu

ENV TS_CONFIG_FILE="/home/model-server/model-store/config.properties"

EXPOSE 8080
EXPOSE 8081
EXPOSE 8082
EXPOSE 7070
EXPOSE 7071

WORKDIR /home/model-server/model-store

COPY ["config.properties", "requirements.txt", "."]

RUN pip install --no-cache-dir -r requirements.txt

COPY ["sdxl.mar", "/tmp/models/"]

CMD ["torchserve", "--model-store=/tmp/models"]