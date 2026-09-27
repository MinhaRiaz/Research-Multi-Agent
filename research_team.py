from crewai import Agent, Crew, Process, Task

from research_manager import create_agent as create_manager
from web_researcher import create_agent as create_web_researcher
from academic_researcher import create_agent as create_academic_researcher
from industry_researcher import create_agent as create_industry_researcher
from research_synthesizer import create_agent as create_synthesizer

def run_single_agent(agent: Agent, description: str, expected_output: str) -> str:
    task = Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )
    result = crew.kickoff()
    return result.raw if hasattr(result, "raw") else str(result)

def run_research(topic: str, depth: str, on_agent_start):
    on_agent_start(0, "Understanding the question and building the research plan.")
    manager = create_manager()
    plan = run_single_agent(
        manager,
        f"""
        User research topic:
        {topic}

        Create a {depth.lower()} research plan.
        Define:
        - the main research question,
        - 5-8 focused subquestions,
        - what should be investigated through general web research,
        - what should be investigated academically,
        - what should be investigated from an industry perspective.

        Use your search tool briefly to identify important scope issues.
        """,
        "A focused research plan with a main question and categorized subquestions.",
    )

    on_agent_start(1, "Searching the live web for broad evidence.")
    web_agent = create_web_researcher()
    web_evidence = run_single_agent(
        web_agent,
        f"""
        Topic: {topic}

        Research plan:
        {plan}

        Conduct broad web research. Find current and relevant evidence.
        Prefer primary/official sources, reputable organizations and high-quality reporting.
        For each major finding include:
        - claim/finding
        - evidence summary
        - source title
        - source URL
        - date if available
        Do not invent facts or URLs.
        """,
        "A structured web evidence report with findings and source URLs.",
    )

    on_agent_start(2, "Searching scholarly sources and academic evidence.")
    academic_agent = create_academic_researcher()
    academic_evidence = run_single_agent(
        academic_agent,
        f"""
        Topic: {topic}

        Research plan:
        {plan}

        Conduct academic-focused research using the scholarly search tool.
        Find relevant papers/studies/reviews where available.
        For useful sources include:
        - title
        - authors when available
        - publication venue/year when available
        - research finding
        - limitations if visible
        - source URL
        Do not fabricate bibliographic details.
        """,
        "A scholarly evidence report with paper details, findings, limitations and URLs.",
    )

    on_agent_start(3, "Investigating companies, products and real-world applications.")
    industry_agent = create_industry_researcher()
    industry_evidence = run_single_agent(
        industry_agent,
        f"""
        Topic: {topic}

        Research plan:
        {plan}

        Investigate real-world industry evidence:
        - companies and organizations
        - products or technologies
        - practical applications
        - adoption examples
        - business/market implications

        Clearly distinguish company claims from independently reported evidence.
        Include source titles and URLs.
        """,
        "An industry evidence report with concrete examples, findings and source URLs.",
    )

    on_agent_start(4, "Validating the evidence and writing the final report.")
    synthesizer = create_synthesizer()
    final_report = run_single_agent(
        synthesizer,
        f"""
        Research topic:
        {topic}

        Research plan:
        {plan}

        GENERAL WEB EVIDENCE:
        {web_evidence}

        ACADEMIC EVIDENCE:
        {academic_evidence}

        INDUSTRY EVIDENCE:
        {industry_evidence}

        Produce the final {depth.lower()} research report.

        Required structure:
        # {topic}

        ## Executive Summary
        Give a concise evidence-based overview.

        ## Key Findings
        Present the most important findings.

        ## Academic Evidence
        Summarize what scholarly evidence indicates.

        ## Industry Perspective
        Summarize companies, products, applications and market evidence.

        ## Analysis
        Compare the evidence and identify patterns or disagreements.

        ## Limitations & Uncertainty
        Explain important evidence gaps, source limitations or conflicting findings.

        ## Conclusion
        Give a neutral synthesis of the evidence.

        ## Sources
        List the source titles and URLs actually used.

        Rules:
        - Do not invent facts, studies, companies or URLs.
        - Distinguish source claims from established findings.
        - If sources disagree, say so rather than forcing agreement.
        - Keep citations/source URLs attached to the relevant evidence where practical.
        """,
        "A polished research report with executive summary, findings, academic evidence, industry perspective, analysis, limitations, conclusion and sources.",
    )

    return final_report
