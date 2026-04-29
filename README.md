# 🌍 Country Guide AI Agent

An intelligent AI-powered country exploration agent that acts as a virtual global tour guide.
It gathers real-time knowledge from Wikipedia and presents it in a friendly, engaging, and structured format.

---

## 🚀 Live Demo  

🔗 View Agent:  https://country-agent-ai-103480118613.europe-west1.run.app/dev-ui/?app=country_guide_agent&session=be5330c8-67bc-4447-ac37-e2e4bb213c33

---

## 🚀 Project Overview

The Country Guide AI Agent is a multi-step AI system built using the Google ADK (Agent Development Kit) and LangChain tools.

It follows a sequential agent workflow:

- Understands the user query
- Fetches country-related data from Wikipedia
- Formats the response into an engaging travel-style explanation

---

## 🧠 Architecture

This project uses a multi-agent architecture with clear separation of responsibilities:

User Input → Root Agent → Research Agent → Formatter Agent → Final Output

🔹 Agents Used

1. Greeter Agent (Root Agent)
- Welcomes the user
- Captures user input
- Stores prompt in shared state
- Triggers the workflow
  
2. Country Researcher Agent
- Uses Wikipedia API via LangChain
- Extracts:
-- Capital
-- Population
-- Geography
-- Culture
-- History
  
3. Response Formatter Agent
- Converts raw data into:
-- Human-friendly explanation
-- Travel-style storytelling
-- Structured output

4. Sequential Workflow
- Ensures agents run in order:
-- Research → Formatting

---

## 🛠️ Tech Stack

- Python
- Google ADK (Agent Development Kit)
- LangChain
- Wikipedia API
- Google Cloud Logging
- dotenv

---

## 📂 Project Structure

- COUNTRY-GUIDE-AGENT/
- │── agent.py            # Main agent logic
- │── requirements.txt    # Dependencies
- │── .env                # Environment variables
- │── __init__.py

---

## 🔍 Key Features

- ✅ Multi-agent architecture
- ✅ Wikipedia-powered real-time knowledge
- ✅ Clean separation of responsibilities
- ✅ Scalable workflow design
- ✅ Conversational AI output
- ✅ Cloud logging support
  
---

### ⭐ Don’t forget to give this project a star if you like it!
