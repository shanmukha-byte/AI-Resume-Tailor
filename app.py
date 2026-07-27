import os
import requests
import streamlit as st

# Page setup
st.set_page_config(
    page_title="AI Resume & Cover Letter Tailor", page_icon="📝"
)

st.title("📝 AI Resume & Cover Letter Tailor")
st.write(
    "Upload your resume details and job description to generate a tailored summary and cover letter."
)

# Inputs
job_description = st.text_area(
    "Paste the Job Description:", height=150
)
user_resume = st.text_area("Paste your Resume / Work Experience:", height=150)

# Hugging Face Inference API Setup (Free & lightweight)
# You can get a free API token from huggingface.co/settings/tokens
HF_API_TOKEN = st.sidebar.text_input(
    "Enter Hugging Face API Key", type="password"
)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"


def query_hf_model(prompt):
  headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
  payload = {
      "inputs": prompt,
      "parameters": {"max_new_tokens": 500, "temperature": 0.7},
  }
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()


if st.button("Generate Tailored Application"):
  if not job_description or not user_resume:
    st.warning("Please fill in both fields.")
  elif not HF_API_TOKEN:
    st.error("Please provide an API Token in the sidebar.")
  else:
    with st.spinner("Generating with Generative AI..."):
      prompt = f"""
            You are a professional career advisor. 
            Job Description: {job_description}
            User Resume: {user_resume}

            Write a professional cover letter and a 3-bullet point resume summary highlighting why the candidate is a fit for this job.
            """

      result = query_hf_model(prompt)

      if isinstance(result, list) and len(result) > 0:
        st.subheader("Your Generated Cover Letter & Resume Summary:")
        st.write(result[0].get("generated_text", "No response generated."))
      else:
        st.error("Failed to generate text. Check your API Token or try again.")