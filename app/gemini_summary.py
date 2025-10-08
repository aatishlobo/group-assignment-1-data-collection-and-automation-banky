from google import genai
from google.genai import types

from user_definition import *

def return_gemini_arxiv_summary(qualification: dict) -> list:
    CUSTOM_SYSTEM_INSTRUCTION = """
    From the given dictionary formatted string,
    summarize artificial intelligence buzzwords in the keys and values as a noun.
    For example,
    "An Evaluation-Centric Paradigm for Scientific Visualization Agents": {
        "Authors": [
            "Kuangshi Ai",
            "Haichao Miao",
            "Zhimin Li",
            "Chaoli Wang",
            "Shusen Liu"
        ],
        "Published": "2025-09-18",
        "Summary": "Recent advances in multi-modal large language models (MLLMs) have enabled\nincreasingly sophisticated autonomous visualization agents capable of\ntranslating user intentions into data visualizations. However, measuring\nprogress and comparing different...",
        "Link": "http://arxiv.org/abs/2509.15160v1"
    }
    This could be represented as an array of string
    ["Evaluation-Centric Paradigm", "Scientific Visualization Agents", "MLLMs", 
    "multi-modal large language models", "Autonomous Visualization Agents"]
    What you need to provide is just a string formatted array, not codes.
    It would be desirable to provide research areas that are relevant to requirements.
    """

    

    client = genai.Client(api_key=gemini_key)
    model_name = "gemini-2.5-flash"

    response = client.models.generate_content(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=CUSTOM_SYSTEM_INSTRUCTION),
        contents=str(qualification)
    )
    return response.text