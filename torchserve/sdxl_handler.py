import logging
import zipfile
from abc import ABC

import numpy as np
import torch
from diffusers import StableDiffusionXLPipeline

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)
logger.info("Loading sdxl_handler...")


class SDXLHandler(BaseHandler, ABC):
    def __init__(self):
        self.initialized = False

    def initialize(self, ctx):
        """In this initialize function, the Stable Diffusion model is loaded and
        initialized here.
        Args:
            ctx (context): It is a JSON Object containing information
            pertaining to the model artefacts parameters.
        """
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")

        logger.info(f"torch.cuda.is_available() = {torch.cuda.is_available()}")
        logger.info(f'gpu_id = {properties.get("gpu_id")}')

        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )

        with zipfile.ZipFile(model_dir + "/sdxl-1.0-model.zip", "r") as zip_ref:
            zip_ref.extractall(model_dir + "/model")

        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_dir + "/model", torch_dtype=torch.bfloat16, variant="fp16"
        )

        self.pipe = self.pipe.to(self.device)

        logger.info(
            f"compiling model for torch > 2.0 ..."
        )
        self.pipe.unet = torch.compile(self.pipe.unet, mode="reduce-overhead", fullgraph=True)
        logger.info(
            f"model compiled successfully..."
        )


        logger.info(
            f"loaded StableDiffusionXL model from {model_dir}/sdxl-1.0-model.zip"
        )

        self.initialized = True

    def preprocess(self, requests):
        """Basic text preprocessing, of the user's prompt.
        Args:
            requests (str): The Input data in the form of text is passed on to the preprocess
            function.
        Returns:
            list : The preprocess function returns a list of prompts.
        """
        inputs = []
        for _, data in enumerate(requests):
            input_text = data.get("data")
            if input_text is None:
                input_text = data.get("body")
            if isinstance(input_text, (bytes, bytearray)):
                input_text = input_text.decode("utf-8")
            logger.info("received text: '%s'", input_text)
            inputs.append(input_text)
        return inputs

    def inference(self, inputs):
        """Generates the image relevant to the received text.
        Args:
            input_batch (list): List of Text from the pre-process function is passed here
        Returns:
            list : It returns a list of the generate images for the input text
        """
        inferences = self.pipe(
            inputs, num_inference_steps=50, height=1024, width=1024
        ).images

        logger.info(f"generated images: {inferences}")
        return inferences

    def postprocess(self, inference_output):
        """Post Process Function converts the generated image into Torchserve readable format.
        Args:
            inference_output (list): It contains the generated image of the input text.
        Returns:
            (list): Returns a list of the images.
        """
        images = []
        for image in inference_output:
            images.append(np.array(image).tolist())
        return images
