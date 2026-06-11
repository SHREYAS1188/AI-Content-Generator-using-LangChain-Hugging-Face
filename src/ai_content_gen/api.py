from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

from prompt_templates import build_prompt
from model import generate
from config import settings

app = FastAPI(title="AI Content Generator", version="0.1")

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="User prompt or instruction")
    model: Optional[str] = Field(None, description="Model name or repo-id to use (e.g., gpt2 or meta-llama/Llama-2-7b-chat-hf)")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(0.9, ge=0.0, le=1.0)
    max_new_tokens: Optional[int] = Field(128, ge=1, le=4096)
    tone: Optional[str] = Field("neutral", description="Tone of the generated content")
    format: Optional[str] = Field("paragraph", description="Output format: paragraph|bullet_points|title_and_paragraph")
    length: Optional[str] = Field("short", description="Desired length: short|medium|long")
    backend: Optional[str] = Field("auto", description="Backend: auto|transformers")

class GenerateResponse(BaseModel):
    model: str
    backend: str
    prompt_used: str
    temperature: float
    top_p: float
    max_new_tokens: int
    generated_text: str
    duration_seconds: float


@app.post("/generate", response_model=GenerateResponse)
async def generate_endpoint(req: GenerateRequest):
    model_name = req.model or settings.DEFAULT_MODEL
    full_prompt = build_prompt(req.prompt, tone=req.tone, format=req.format, length=req.length)

    start = time.time()
    try:
        text = generate(model_name=model_name,
                        prompt=full_prompt,
                        temperature=req.temperature,
                        top_p=req.top_p,
                        max_new_tokens=req.max_new_tokens,
                        backend=req.backend)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    duration = time.time() - start

    return GenerateResponse(
        model=model_name,
        backend=req.backend or "auto",
        prompt_used=full_prompt,
        temperature=req.temperature,
        top_p=req.top_p,
        max_new_tokens=req.max_new_tokens,
        generated_text=text,
        duration_seconds=duration
    )

