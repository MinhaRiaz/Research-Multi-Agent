import os
from crewai_tools import SerperDevTool

def _check_key():
    if not os.getenv("SERPER_API_KEY"):
        raise RuntimeError("SERPER_API_KEY is missing. Add it to Streamlit Secrets.")

def web_search_tool():
    _check_key()
    return SerperDevTool(
        n_results=6,
        search_url="https://google.serper.dev/search",
    )

def academic_search_tool():
    _check_key()
    return SerperDevTool(
        n_results=6,
        search_url="https://google.serper.dev/scholar",
    )
