from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json
from googleapiclient.discovery import build

app = FastAPI()

# Define the request data model
class RequestData(BaseModel):
    question: str
    form_data: Dict

# Google Custom Search API credentials
GOOGLE_API_KEY = "AIzaSyB5K70aH9juc5SHMdu_YH6Dq-4RIA64OkE"
SEARCH_ENGINE_ID = "d3bbf6336abdc4017"

# Function to get website links and descriptions using Google Custom Search API
def GoogleSearch_links_with_description(query, num_results=3):
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=num_results).execute()
        links_data = []
        for item in result.get("items", []):
            link_info = {
                "title": item.get("title"),
                "link": item["link"],
                "snippet": item.get("snippet")
            }
            links_data.append(link_info)
        return links_data
    except Exception as e:
        print(f"Error during Google Custom Search API call: {e}")
        return []

# Endpoint to generate chatbot response
@app.post("/generate_response")
async def generate_response(data: RequestData):
    try:
        # --- Setup and Initial Data ---
        # OpenAI Key
        os.environ["OPENROUTER_API_KEY"] = "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"

        # Web Search for Initial Context using Google Custom Search API
        city_name = data.form_data.get("city_name", "Bengaluru")
        income = data.form_data.get("income_range", "Middle Class")
        initial_search_query = f"energy saving tips in {city_name} for {income} households"
        search_results = GoogleSearch_links_with_description(initial_search_query)
        search_context = " ".join([item['snippet'] for item in search_results[:3] if item.get('snippet')]) if isinstance(search_results, list) else search_results

        # --- LLM Chain for Main Response ---
        prompt_template = PromptTemplate(
            input_variables=["question", "form_data", "search_context", "city_name"],
            template="""You are EcoSenseAI, a friendly and helpful AI chatbot designed to assist homeowners in {city_name} with saving energy and money. You now have access to the context from web searches, use it to provide a better answer.

Your primary function is to provide personalized and actionable advice based on the user's energy assessment form data.

When a user asks a question:
* If the question is directly related to energy saving or their home energy usage: Use the information provided in the 'Form data', and the search_context to give specific and practical recommendations. Consider the local climate in {city_name}. Structure your response clearly, potentially with an encouraging opening, tailored tips (with reasoning if possible), and a friendly closing.
* If the question is unrelated to energy saving: Briefly acknowledge that the question is outside your area of expertise as EcoSenseAI. Then, if appropriate, gently steer the conversation back to energy saving.
* If the user expresses gratitude: Respond with a polite acknowledgment.

Here is the user's question: {question}

Here is the information they provided about their home and energy usage:
{form_data}

Here is some additional context from web searches:
{search_context}

Please provide a response that adheres to these guidelines, keeping the interaction natural and focused on the user's intent. If using data from web searches, make sure to add a disclaimer that the advice is taken from web searches and it is not a substitute for a professional energy audit.
""",
        )
        llm = ChatOpenAI(temperature=0.7, model_name="meta-llama/llama-4-maverick:free", openai_api_base="https://openrouter.ai/api/v1", openai_api_key=os.environ["OPENROUTER_API_KEY"])
        llm_chain = LLMChain(prompt=prompt_template, llm=llm)
        response = await llm_chain.arun(question=data.question, form_data=data.form_data, search_context=search_context, city_name=city_name)

        # --- LLM Chain for Follow-Up Questions ---
        followup_prompt_template = PromptTemplate(
            input_variables=["question", "form_data", "search_context", "city_name"],
            template="""Generate a JSON array containing exactly 3 follow-up questions that a user in {city_name} might ask after receiving an initial response about saving energy, considering their question: "{question}" and the following information: {form_data}. The questions should be relevant and encourage further interaction on energy saving. Ensure the output is a valid JSON array of strings. Do not include any markdown formatting like ```json. Just output the raw JSON array.
""",
        )
        followup_chain = LLMChain(prompt=followup_prompt_template, llm=llm)
        followup_questions_str = await followup_chain.arun(question=data.question, form_data=data.form_data, search_context=search_context, city_name=city_name)

        # Remove markdown formatting from follow-up questions
        followup_questions_str = followup_questions_str.strip()
        if followup_questions_str.startswith("```json") and followup_questions_str.endswith("```"):
            followup_questions_str = followup_questions_str[len("```json"): -len("```")].strip()
        elif followup_questions_str.startswith("```") and followup_questions_str.endswith("```"):
            followup_questions_str = followup_questions_str[len("```"): -len("```")].strip()

        # Try to parse the follow-up questions string as a JSON array
        try:
            followup_questions = json.loads(followup_questions_str)
            if not isinstance(followup_questions, list):
                followup_questions = [followup_questions_str] # If not a list, treat as a single question
        except json.JSONDecodeError as e:
            print(f"Error parsing follow-up questions JSON: {e}")
            followup_questions = [followup_questions_str] # If parsing fails, treat as a single question

        # --- LLM Chain for Generating Search Queries ---
        # --- LLM Chain for Generating Search Queries ---
        search_query_prompt_template = PromptTemplate(
            input_variables=["question", "followup_questions"],
            template="""Based on the initial question: "{question}" and these follow-up questions: {followup_questions}, your task is to generate exactly 3 distinct and highly relevant search queries. These search queries should be specifically designed to find information that can directly answer the follow-up questions.

Consider the following guidelines when creating the search queries:

* **Focus on answering the follow-up questions:** Each search query should aim to target a specific aspect or question raised in the 'follow-up questions'.
* **Be specific and clear:** Formulate queries that are likely to yield precise and informative results. Use keywords and phrases that accurately reflect the user's needs.
* **Explore different angles:** Try to think of different ways a user might phrase their search if they were looking for answers to these follow-up questions. Consider synonyms and related terms.
* **Keep them concise:** While being specific, ensure the queries are not overly long or complex. Shorter, well-targeted queries often perform best in search engines.
* **Avoid conversational language:** The search queries should be in the format that you would typically type into a search engine (e.g., keywords, short phrases, or specific questions).
* **Relevance to the initial question:** While focusing on the follow-up questions, ensure the search queries are still broadly related to the initial question asked by the user.

Return these 3 search queries as a JSON array of strings. Do not include any explanations, markdown formatting, or any text outside of the JSON array. Just output the raw JSON array.
""",
        )
        search_query_chain = LLMChain(prompt=search_query_prompt_template, llm=llm)
        search_queries_str = await search_query_chain.arun(question=data.question, followup_questions=json.dumps(followup_questions))

        # Remove markdown formatting from search queries
        search_queries_str = search_queries_str.strip()
        if search_queries_str.startswith("```json") and search_queries_str.endswith("```"):
            search_queries_str = search_queries_str[len("```json"): -len("```")].strip()
        elif search_queries_str.startswith("```") and search_queries_str.endswith("```"):
            search_queries_str = search_queries_str[len("```"): -len("```")].strip()

        # Try to parse the search queries string as a JSON array
        try:
            search_queries = json.loads(search_queries_str)
            if not isinstance(search_queries, list):
                search_queries = [search_queries_str]
        except json.JSONDecodeError as e:
            print(f"Error parsing search queries JSON: {e}")
            search_queries = [search_queries_str]

        # --- Perform Google Search for Links with Description using the API ---
        website_links = []
        if isinstance(search_queries, list):
            for query in search_queries:
                links_data = GoogleSearch_links_with_description(query)
                website_links.extend(links_data)

        print(f"Response\n{response}\nFollowUp Questions\n{followup_questions}\nWebsite Links\n{website_links}")
        return {"response": response, "followup_questions": followup_questions, "website_links": website_links[:5]}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))