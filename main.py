import streamlit as st
from pages import home, form, chatbot


PAGES = {
    "Home": home,
    "Form": form,
    "Chatbot": chatbot,
}


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    page.run()

if __name__ == "__main__":
    #remove title
    st.markdown("<style>div[data-testid='stSidebarNav'] ul { display: none; }</style>", unsafe_allow_html=True)
    main()

    ## Ask the home page to be updated accordingly to accomodate 
    # the new ideas 