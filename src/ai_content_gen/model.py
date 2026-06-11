from functools import lru_cache
from typing import Optional, Dict, Any
import os
import torch

from transformers import pipeline, GenerationConfig
from config import settings

# When used as a package, ensure relative imports work

@lru_cache(maxsize=8)
def _create_pipeline(model_name: str, device: int = -1):
    """Create and cache a text-generation pipeline.
    device: -1 for CPU, >=0 for CUDA device id (if available)
    """
    # Set device id for transformers pipeline
    device_id = -1
    if device >= 0 and torch.cuda.is_available():
        device_id = int(device)

    pipe = pipeline(
        "text-generation",
        model=model_name,
        tokenizer=model_name,
        device=device_id,
        trust_remote_code=True,
    )
    return pipe


def generate_with_transformers(model_name: str,
                               prompt: str,
                               temperature: float = 0.7,
                               top_p: float = 0.9,
                               max_new_tokens: int = 128,
                               device: int = settings.DEVICE,
                               **kwargs) -> str:
    pipe = _create_pipeline(model_name, device=device)
    gen_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        **kwargs,
    )
    outputs = pipe(prompt, generation_config=gen_config, return_full_text=False)
    if isinstance(outputs, list) and len(outputs) > 0:
        return outputs[0].get("generated_text", "")
    # Fallback string
    return str(outputs)


def generate(model_name: str,
             prompt: str,
             temperature: float = 0.7,
             top_p: float = 0.9,
             max_new_tokens: int = 128,
             backend: str = "auto",
             **kwargs) -> str:
    """Unified generate function. backend can be: auto|transformers.
    We avoid calling HuggingFaceHub via LangChain inside this simple production layout to
    keep dependencies predictable. The code is ready to extend to HF Hub when a token is present.
    """
    # Decide backend
    if backend == "auto":
        if settings.USE_HF_HUB and (settings.HUGGINGFACEHUB_API_TOKEN or os.getenv("HUGGINGFACEHUB_API_TOKEN")):
            # Prefer transformers pipeline for local or remote repo loading; users can set model to a HF repo id.
            backend = "transformers"
        else:
            backend = "transformers"

    if backend == "transformers":
        return generate_with_transformers(model_name, prompt, temperature=temperature, top_p=top_p, max_new_tokens=max_new_tokens, **kwargs)

    # Unknown backend
    raise ValueError(f"Unsupported backend: {backend}")

