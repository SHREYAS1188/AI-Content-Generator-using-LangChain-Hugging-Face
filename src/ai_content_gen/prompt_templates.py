from typing import Literal

BASE_TEMPLATE = """
You are an expert content writer and editor. Follow the instructions precisely.

Instruction:
{instruction}

Tone: {tone}
Format: {format}
Length: {length}

Provide the content only. Do not include analysis or extraneous commentary.
"""


def build_prompt(user_prompt: str,
                 tone: str = "neutral",
                 format: Literal["paragraph", "bullet_points", "title_and_paragraph"] = "paragraph",
                 length: str = "short") -> str:
    """
    Constructs a full prompt from a user prompt and metadata.
    - tone: neutral, professional, casual, humorous
    - format: paragraph | bullet_points | title_and_paragraph
    - length: short | medium | long
    """
    instruction = user_prompt.strip()
    return BASE_TEMPLATE.format(instruction=instruction, tone=tone, format=format, length=length)

