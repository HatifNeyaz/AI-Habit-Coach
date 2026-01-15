# 🚀 AI Habit Builder & Routine Optimizer
An intelligent productivity agent that researches and designs your day using high-speed LLMs.

### 📖 Project Overview
The AI Habit Builder is a data-driven application designed to transform vague goals into actionable, research-backed routines. Unlike standard to-do apps, this tool acts as a "Productivity Scientist." It analyzes your profile, identifies efficiency gaps, and searches the web for the best methods (like Pomodoro or Time Blocking) and resources (YouTube/Web) to help you succeed.

### 🛠️ Tech Stack
LLM Engine: Groq (Llama 3.3 70B) for lightning-fast reasoning.

Orchestration: LangChain for agentic workflow management.

Research Tool: DuckDuckGo Search API for real-time web access.

Frontend: Streamlit (Layout: Wide) for a professional dashboard experience.

Data Validation: Pydantic for structured JSON-to-table parsing.

### ✨ Key Features
Personalized Coaching: Analyzes "bad habits" and suggests specific replacements.

Web-Augmented Suggestions: Directly pulls YouTube links and website recommendations tailored to your goals.

Flexible Modes: Choose between redesigning your existing routine or letting the AI build one from scratch.

Export Ready: Instantly download your new schedule as a clean CSV file.

# Flowchart
```mermaid
graph TD
    A[User Input: Bio & Tasks] --> B{Groq AI Agent}
    B --> C[Web Search: DuckDuckGo]
    C --> D[Identify Productivity Methods]
    D --> E[Llama 3.3 Reasoning]
    E --> F[Pydantic Structured Output]
    F --> G[Streamlit Wide UI]
    G --> H[CSV Export]
    
    % Professional Styling
    style A font-weight:bold,color:#fff,font-size:16px
    style B fill:#f9f,stroke:#333,stroke-width:2px,font-weight:bold,color:#000,font-size:16px
    style C font-weight:bold,color:#fff,font-size:16px
    style D font-weight:bold,color:#fff,font-size:16px
    style E fill:#bbf,stroke:#333,stroke-width:2px,font-weight:bold,color:#000,font-size:16px
    style F font-weight:bold,color:#fff,font-size:16px
    style G fill:#dfd,stroke:#333,stroke-width:2px,font-weight:bold,color:#000,font-size:16px