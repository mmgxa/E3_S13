from diffusers import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.bfloat16, variant="fp16", use_safetensors=True
)

pipe.save_pretrained("./sdxl-1.0-model")