import streamlit as st
import streamlit.components.v1 as components
import json

def load_lottiefile(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def run():
    st.title("Welcome to EcoSense AI: Your Smart Home Energy Advisor")

    st.write("--- ")

    st.header("What is EcoSense AI?")
    col1, col2 = st.columns([1, 1],border=True)
    with col1:
        st.write("EcoSense AI is an innovative chatbot designed to empower homeowners with personalized, context-aware advice for making more responsible and sustainable energy consumption choices within their households.")
        st.write("Our goal is to guide you towards reducing your energy footprint, saving money on utility bills, and contributing to a more environmentally friendly future.")

        st.write("--- ")

        st.subheader("Ready to Get Started?")
        st.write("Fill out the Energy Assessment Form now and start your journey towards a more sustainable and energy-efficient home!")
        st.write("[Go to the Form in the Navigator Pane](Form)")  # Link to the Form page
    with col2:
        st.markdown("""
        ## Tired of Energy Bills That Make You 🤯?

        Fear not! EcoSense AI is here to help you become an energy-saving 🦸!

        We'll turn your energy bill from a 😭 into a 😄 (or at least a 😐).

        Get ready to:
        *   💰 Save some serious cash
        *   🌍 Help the planet (because it's the only one we've got!)
        *   💡 Discover the secrets to a more energy-efficient home
        """)

    st.write("--- ")

    st.header("How Does EcoSense AI Work?")
    st.subheader("1. Energy Assessment Form")
    st.write("Start by filling out our comprehensive energy assessment form. This form gathers information about your home, appliances, energy consumption habits, and existing energy-saving measures.")

    st.subheader("2. AI-Powered Analysis")
    st.write("Your responses are then analyzed by our intelligent chatbot, which uses LangChain and a powerful Large Language Model (LLM) to understand your energy profile.")

    st.subheader("3. Personalized Recommendations")
    st.write("Based on the analysis, EcoSense AI provides you with tailored advice and actionable steps to reduce your energy consumption, save money, and improve your home's energy efficiency.")

    st.write("--- ")

    st.header("Benefits of Using EcoSense AI")
    st.write("- **Save Money:** Identify opportunities to reduce your energy bills.")
    st.write("- **Reduce Energy Consumption:** Lower your environmental impact by using less energy.")
    st.write("- **Promote Sustainability:** Contribute to a more sustainable future for yourself and your community.")
    st.write("- **Personalized Advice:** Get tailored recommendations based on your specific home and energy usage.")
    st.write("- **Easy to Use:** Interact with our intuitive chatbot interface.")