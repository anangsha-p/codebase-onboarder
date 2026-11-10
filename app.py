import os
import sys
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

st.set_page_config(page_title="Codebase Onboarder AI", layout="wide")
st.title("Codebase Onboarder AI")
st.caption("Ask a question about an indexed repo and get an answer with file and line citations.")

repo = st.text_input("Indexed repo name", value="flask")
question = st.text_input("Your question", placeholder="Where is the development server started?")

if st.button("Ask") and question.strip():
    with st.spinner("Loading models, searching the code and asking Gemini..."):
        try:
            from qa import answer
            text, chunks = answer(repo, question)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.subheader("Answer")
    st.markdown(text)

    st.subheader("Sources")
    for code, m in chunks:
        label = f"{m['path']} | {m['name']} | lines {m['start']}-{m['end']}"
        with st.expander(label):
            st.code(code, language="python")