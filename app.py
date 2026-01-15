import streamlit as st
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.tools import DuckDuckGoSearchRun

# --- 1. THE SCHEMA (The AI's Output Template) ---
class HabitTask(BaseModel):
    task_name: str = Field(description="Name of the activity")
    time: str = Field(description="Time in 12hr AM/PM format (e.g. 09:00 AM)")
    category: str = Field(description="Productive, Routine, or Leisure")
    coach_note: str = Field(description="Explanation of why this task is here under 20 words")
    links_recommendations: str = Field(description="websites, YouTube link or website for learning the task")

class Routine(BaseModel):
    tasks: List[HabitTask]

# --- 2. THE UI CONFIGURATION ---
st.set_page_config(page_title="AI Habit Builder", page_icon="📝", layout= "wide")
st.title("🚀 AI Habit Builder")

# Step 1: Groq API Key
with st.expander("🔑 Step 1: Set up Groq API Key", expanded=True):
    api_key = st.text_input("Enter your Groq API Key:", type="password")

if not api_key:
    st.warning("Please enter your API key to continue.")
    st.stop() # This stops the app from running further code

# Step 2: User Profile
st.header("📝 Tell us about yourself")
user_bio = st.text_area(
    "What do you do? What are your goals? Any bad habits?",
    placeholder="Example: I'm a student who wants to learn coding but I spend too much time on Instagram."
)

# Step 3: Choose Mode and Input Tasks
st.header("📅 Your Routine")
mode = st.radio("How would you like to build your routine?", 
                ["Redesign my current list", "AI-designed routine (from scratch)"])

current_tasks = ""
if mode == "Redesign my current list":
    current_tasks = st.text_area("List your tasks and timings:", 
                                 placeholder="8am - Wake up\n9am - Breakfast...")

search = DuckDuckGoSearchRun()
search_query = f"best productivity methods and YT channels for someone who: {user_bio}"
research_results = search.run(search_query)
#--- 3. THE LOGIC (The Brain) ---
if st.button("Generate/Redesign Routine"):
    if not user_bio:
        st.error("Please fill out the 'About yourself' section!")
    else:
        with st.spinner("Our AI Coach is analyzing your day..."):
            try:
                # Initialize LLM
                llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
                parser = PydanticOutputParser(pydantic_object=Routine)

                # The Prompt with Conditional Logic
                prompt_text = (
                    "You are a World-Class Productivity Coach. You will not only help in providing the task but also the link and productive videos and playlists so that user is benefited\n"
                    "User Bio: {bio}\n"
                    "Provided Routine: {tasks}\n\n"
                    "Use this RESEARCH to help the user: {research}\n"
                    "TASK: If 'Provided Routine' is empty, create a full daily routine from scratch based on the bio. "
                    "If 'Provided Routine' has content, redesign it to be more productive. "
                    "Identify gaps for high-value skills and eliminate bad habits mentioned in the bio."
                    "\n\n{format_instructions}"
                )

                prompt = ChatPromptTemplate.from_template(prompt_text)
                chain = prompt | llm | parser

                # Run Chain
                result = chain.invoke({
                    "research": research_results,
                    "bio": user_bio,
                    "tasks": current_tasks if current_tasks else "None provided",
                    "format_instructions": parser.get_format_instructions()
                })

                # Display Results
                df = pd.DataFrame([t.dict() for t in result.tasks])
                st.subheader("✅ Your Optimized Routine")
                st.dataframe(df, use_container_width=True)

                # CSV Download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Routine as CSV", data=csv, 
                                   file_name="ai_routine.csv", mime="text/csv")

            except Exception as e:
                st.error(f"Something went wrong: {e}")