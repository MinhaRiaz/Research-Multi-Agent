from crewai import Agent
from llm_config import get_llm
from research_tools import web_search_tool

def create_agent():
    return Agent(
        role="Research Manager",
        goal="Understand the user's research question and create a focused plan covering web, academic and industry evidence.",
        backstory=(
            "You are a senior research manager. You clarify the scope, identify the important dimensions "
            "of a topic and create a practical research plan. Use web search to identify blind spots before planning."
        ),
        tools=[web_search_tool()],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
