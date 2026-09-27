# ResearchForge AI

A simple modular CrewAI multi-agent research application using Gemini 3.8 Flash, Serper web search, and Streamlit.

## Agents

1. Research Manager — understands the question and plans the research
2. Web Researcher — broad web research
3. Academic Researcher — papers and scholarly evidence
4. Industry Researcher — companies, products, market and applications
5. Research Synthesizer — verifies evidence and writes the final report

## Required Streamlit Secrets

```toml
GEMINI_API_KEY = "your-gemini-key"
SERPER_API_KEY = "your-serper-key"
```

## Deployment

Upload the files to GitHub and deploy `app.py` on Streamlit Community Cloud with Python 3.12.
No local installation is required for the deployment workflow.
