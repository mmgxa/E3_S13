

```
pip install transformers diffusers --upgrade
pip install invisible_watermark transformers accelerate safetensors --upgrade
```

Check for bf16 support

```
python -c 'import transformers; print(f"BF16 support is {transformers.file_utils.is_torch_bf16_gpu_available()}")',
```

```
python torchserve.py
```

```
sudo apt install zip
```

```
cd sdxl-1.0-model
zip -0 -r ../sdxl-1.0-model.zip *
```


## Create MAR file
```
docker pull pytorch/torchserve:latest-gpu

docker run -it --rm --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -v `pwd`:/opt/src pytorch/torchserve:latest-gpu bash

cd /opt/src
torch-model-archiver --model-name sdxl --version 1.0 --handler sdxl_handler.py --extra-files sdxl-1.0-model.zip -r requirements.txt
```

## Run Torchserve in Docker
```
docker build -t emlo:s13 . --no-cache 
docker run --rm --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 --gpus all -p8080:8080 -p8081:8081 -p8082:8082 -p7070:7070 -p7071:7071 emlo:s13
```


```
curl "http://localhost:8081/models"
```


```
python test_endpoint.py
```

