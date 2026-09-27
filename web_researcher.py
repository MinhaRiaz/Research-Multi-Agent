from crewai import Agent
from llm_config import get_llm
from research_tools import web_search_tool

def create_agent():
    return Agent(
        role="Web Researcher",
        goal="Conduct broad current web research and collect reliable evidence relevant to the research plan.",
        backstory=(
            "You are a professional web researcher. Search broadly but prioritize official sources, "
            "reputable organizations, high-quality reporting and direct evidence. Always retain source titles and URLs."
        ),
        tools=[web_search_tool()],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
