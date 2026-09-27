from crewai import Agent
from llm_config import get_llm
from research_tools import web_search_tool

def create_agent():
    return Agent(
        role="Research Synthesizer",
        goal="Verify the team's evidence, resolve conflicts where possible, state uncertainty clearly, and produce the final research report.",
        backstory=(
            "You are a rigorous research synthesizer and writer. You compare evidence from the web, academic "
            "and industry researchers, use search when a key claim needs verification, and never invent citations. "
            "You distinguish established evidence, source claims and reasonable interpretation."
        ),
        tools=[web_search_tool()],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
