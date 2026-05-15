# 🚀 Agentic Sales Pipeline

An enterprise-grade, fully automated AI sales pipeline built using [CrewAI](https://crewai.com/). This project uses multiple specialized AI agents to research leads, score them based on predefined rubrics, and draft highly personalized outreach emails.

## 🏗️ Architecture

This project is built using the **CrewAI Flow** architecture, acting as a smart gatekeeper to save API tokens and compute costs. It consists of two distinct Crews:

### 1. The Lead Scoring Crew
A team of 3 agents responsible for researching and qualifying incoming leads:
- **Lead Data Specialist:** Uses web search tools to gather personal and company data on the lead.
- **Cultural Fit Analyst:** Evaluates how well the lead's company aligns with our product's mission and values.
- **Scoring Validator:** Aggregates the research and outputs a strict, Pydantic-structured `LeadScoringResult` with a final score from 0-100.

### 2. The Flow Orchestrator (Gatekeeper)
The pipeline is managed by a `SalesPipeline(Flow)` class. 
The Flow takes the structured output from the Lead Scoring Crew and filters out any leads with a score of less than 70. **Only highly-qualified leads (>70)** are passed to the next phase, preventing wasted LLM tokens on bad leads.

### 3. The Email Writing Crew
A team of 2 agents responsible for crafting the outreach:
- **Email Content Specialist:** Drafts a highly personalized email based on the lead's background and company info.
- **Engagement Strategist:** Optimizes the draft to ensure strong Hooks and Call-To-Actions (CTAs) for maximum conversion.

## 💸 Cost Tracking
The pipeline includes built-in telemetry to track API costs for both Crews independently. It extracts `token_usage` metrics (splitting prompt tokens and completion tokens) to calculate exact API expenditures based on DeepSeek pricing models.

## 🛠️ Setup & Installation
1. Clone the repository
2. Install dependencies: `uv pip install crewai crewai-tools pandas`
3. Create a `.env` file in the root directory with your API keys:
   ```env
   OPENAI_API_KEY=your_key
   SERPER_API_KEY=your_key
   ```
4. Run the pipeline:
   ```bash
   python sales_pipeline.py
   ```
