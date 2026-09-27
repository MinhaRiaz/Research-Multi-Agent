from crewai import Agent
from llm_config import get_llm
from research_tools import web_search_tool

def create_agent():
    return Agent(
        role="Industry Researcher",
        goal="Investigate companies, products, market applications, adoption patterns and real-world industry use cases.",
        backstory=(
            "You are an industry research analyst. Look for company announcements, product documentation, "
            "market applications, credible business reporting and concrete examples of real-world adoption. "
            "Separate company claims from independently reported evidence."
        ),
        tools=[web_search_tool()],
        llm=get_llm(),
        verbose=False,
        allow_delegation=False,
    )
