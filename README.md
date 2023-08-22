<div align="center">

# Session 13

</div>

In this session, we deploy a Stable Diffusion XL (SDXL) model behind a FastAPI backend on EC2 Mode. The frontend is made with Next.JS and is hosted on Vercel. 

## Download/Save Model

```
python torchserve.py
```

Since a g5 instance with A10 is being used, the `bfloat16` data type has been used!


## Create MAR file
```
docker pull pytorch/torchserve:latest-gpu

docker run -it --rm --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v `pwd`:/opt/src pytorch/torchserve:latest-gpu bash

cd /opt/src
torch-model-archiver --model-name sdxl --version 1.0 --handler sdxl_handler.py --extra-files sdxl-1.0-model.zip -r requirements.txt
```


We then create a Docker image for TorchServe that bundles the container.

```
docker build -t emlo:s13 . --no-cache 
```


## Docker Compose

We then package TorchServe, FastAPI, and Caddy into a docker compose file. They are started using

```
docker compose up
```

The frontend has been deployed to vercel.


## UI


https://github.com/mmgxa/E3_S13/assets/83439262/24c79e24-fb15-46f2-8112-50b35c4d7910

