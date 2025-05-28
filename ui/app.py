import streamlit as st
import requests

# Title and description
st.title("🧠 CloudDocs AI Assistant")
st.markdown("Ask any question about Microsoft Azure docs — powered by GPT-4o + Pinecone")

# Render API endpoint (change this to your actual URL)
API_URL = "https://cloudocs-ai-agent.onrender.com/ask"

# Input form
question = st.text_input("Ask your question about Azure:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    st.success("Answer:")
                    st.markdown(data["answer"])

                    st.markdown("---")
                    st.markdown("**Sources:**")
                    for src in data["sources"]:
                        lines = src.split("\n")
                        if len(lines) >= 2:
                            st.markdown(f"- [{lines[0]}]({lines[1]})")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
