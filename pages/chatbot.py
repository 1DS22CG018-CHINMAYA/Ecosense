import streamlit as st
import requests
import uuid
import json
import pandas as pd

def run():
    st.title("EcoSense AI Chatbot")
    st.write("Welcome to the EcoSense AI chatbot. Ask me anything about saving energy!")

    if "form_data" in st.session_state:
        form_data = st.session_state["form_data"]

        st.header("User's Consumption Profile")

        with st.container():
            st.subheader("Key Metrics:")
            col1, col2 = st.columns(2,border=True)
            col1.write(f"**Total Energy Consumed:** {form_data['kwh_consumed']} kWh")
            col2.write(f"**Energy Cost:** {form_data['energy_cost']}")
            col1.write(f"**Number of Occupants:** {form_data['num_occupants']}")
            col2.write(f"**Dwelling Type:** {form_data['dwelling_type']}")

            st.subheader("Additional Details:")
            for key, value in form_data.items():
                if key not in ["kwh_consumed", "energy_cost", "num_occupants", "dwelling_type", "city_name", "income_range"]:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")

            # You can add more decorative elements or arrange the layout further within the container
            # For instance, you could use st.columns again for the additional details

        st.write("--- ")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Generate session ID if not already in session state
        if "session_id" not in st.session_state:
            st.session_state["session_id"] = str(uuid.uuid4())

        # Display chat history
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me about saving energy:", key="main_chat_input"):
            # Add user message to chat history
            st.session_state["chat_history"].append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Send data to FastAPI API
            api_url = "http://localhost:8000/generate_response"  # Replace with your API URL if different
            data = {"question": prompt, "form_data": form_data}
            try:
                response = requests.post(api_url, json=data)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                result = response.json()
                bot_response = result["response"]
                followup_questions = result.get("followup_questions", [])
                website_links = result.get("website_links", []) # Get website links
            except requests.exceptions.RequestException as e:
                bot_response = f"Error: Could not connect to API - {e}"
                followup_questions = []
                website_links = []
            except json.JSONDecodeError as e:
                bot_response = f"Error: Could not decode JSON from API - {e}"
                followup_questions = []
                website_links = []

            # Add bot message to chat history
            st.session_state["chat_history"].append({"role": "assistant", "content": bot_response})
            # Display bot message in chat message container
            with st.chat_message("assistant"):
                st.markdown(bot_response)

            # Display relevant website links with title and description
            if website_links:
                st.markdown("**Relevant Resources as searched from the google 🔵🔴🟡🟢: It is always better to know more🔍**")
                for link_info in website_links:
                    title = link_info.get("title", "No Title Available")
                    link_url = link_info.get("link", "#")
                    snippet = link_info.get("snippet", "No Description Available")
                    st.markdown(f"* ✅[{title}]({link_url}) - {snippet}", unsafe_allow_html=True)

            # Display follow-up questions as bullet points
            if followup_questions:
                st.markdown("**Follow-Up Questions:** 🙋☝")
                for question in followup_questions:
                    st.markdown(f"👉 {question}")

    else:
        st.warning("Please fill out the energy assessment form first.")

if __name__ == "__main__":
    run()