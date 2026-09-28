import os
from crewai import LLM


def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to Streamlit Secrets."
        )

    return LLM(
        model="gemini/gemini-3.8-flash",
        api_key=api_key,
    )
