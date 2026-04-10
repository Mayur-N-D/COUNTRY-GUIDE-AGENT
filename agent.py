import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# Greet user and save their prompt

def add_prompt_to_state(
    tool_context: ToolContext, prompt: str
) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[State updated] Added to PROMPT: {prompt}")
    return {"status": "success"}

# Configuring the Wikipedia Tool
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# 1. Researcher Agent
country_researcher = Agent(
    name="country_researcher",
    model=model_name,
    description="The primary researcher that accesses external knowledge about countries from Wikipedia.",
    instruction="""
    You are a helpful geographic and historical research assistant. Your goal is to fully answer the user's PROMPT about a specific country, region, or culture.
    
    You have access to a Wikipedia search tool. 
    - First, analyze the user's PROMPT to identify the country or geographic topic they are asking about.
    - Use the Wikipedia tool to gather comprehensive information (e.g., capital city, population, history, geography, culture, and interesting facts).
    - Synthesize the results from the tool into preliminary data outputs.

    PROMPT:
    { PROMPT }
    """,
    tools=[
        wikipedia_tool
    ],
    output_key="research_data" # A key to store the combined findings
)

# 2. Response Formatter Agent
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="Synthesizes all information into a friendly, readable response.",
    instruction="""
    You are the friendly voice of a Global Tour Guide. Your task is to take the
    RESEARCH_DATA and present it to the user in a complete, engaging, and helpful answer.

    - First, present the core facts about the country (like location, capital, and population).
    - Then, highlight interesting historical, cultural, or geographical facts from the research.
    - If some specific information is missing, just present the information you have clearly.
    - Be conversational, inspiring, and engaging, as if you are planning a trip for them.

    RESEARCH_DATA:
    { research_data }
    """
)

# 3. Sequential Workflow
country_guide_workflow = SequentialAgent(
    name="country_guide_workflow",
    description="The main workflow for handling a user's request about a country.",
    sub_agents=[
        country_researcher, # Step 1: Gather all data about the country
        response_formatter, # Step 2: Format the final response
    ]
)

# 4. Root Agent (Greeter)
root_agent = Agent(
    name="greeter",
    model=model_name,
    description="The main entry point for the Country Guide AI.",
    instruction="""
    - Greet the user warmly and let them know you are their virtual Global Tour Guide, here to help them learn about any country or region in the world.
    - When the user responds with their destination or question, use the 'add_prompt_to_state' tool to save their response.
    - After using the tool, transfer control to the 'country_guide_workflow' agent so it can begin researching.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[country_guide_workflow]
)