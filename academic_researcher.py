from crewai import Agent
from llm_config import get_llm
from research_tools import academic_search_tool

def create_agent():
    return Agent(
        role="Academic Researcher",
        goal="Find and summarize relevant academic papers and scholarly evidence related to the research topic.",
        backstory=(
            "You are an academic research specialist. Search scholarly sources, identify useful studies, "
            "and distinguish empirical evidence from commentary. Record paper titles, authors when available, "
            "publication information and URLs."
        ),
        tools=[academic_search_tool()],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
