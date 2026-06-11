import streamlit as st
import requests
import time
from typing import Dict, Any

st.set_page_config(page_title="AI Content Generator", layout="centered")

API_URL = st.sidebar.text_input("API URL", value="http://localhost:8000/generate")
st.sidebar.markdown("Make sure the FastAPI backend is running at this URL.")

st.title("AI Content Generator")
st.markdown("Use the controls below to build prompts and generate content via your LangChain + Hugging Face backend.")

with st.form("generate_form"):
    prompt = st.text_area("Prompt / Instruction", height=160, placeholder="Write a marketing blurb about...")

    col1, col2 = st.columns(2)
    with col1:
        model = st.text_input("Model", value="gpt2", help="Model name or repo id (eg. gpt2 or meta-llama/Llama-2-7b-chat-hf)")
        tone = st.selectbox("Tone", ["neutral", "professional", "casual", "humorous"], index=0)
        fmt = st.selectbox("Format", ["paragraph", "bullet_points", "title_and_paragraph"], index=0, label="Format")
    with col2:
        length = st.selectbox("Length", ["short", "medium", "long"], index=0)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.01)
        top_p = st.slider("Top-p (nucleus sampling)", min_value=0.0, max_value=1.0, value=0.9, step=0.01)

    max_new_tokens = st.number_input("Max new tokens", min_value=1, max_value=4096, value=128, step=1)
    backend = st.selectbox("Backend", ["auto", "transformers"], index=0)
    submit = st.form_submit_button("Generate")

if submit:
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "model": model or None,
            "temperature": float(temperature),
            "top_p": float(top_p),
            "max_new_tokens": int(max_new_tokens),
            "tone": tone,
            "format": fmt,
            "length": length,
            "backend": backend,
        }

        st.info("Sending generation request...")
        start = time.time()
        try:
            resp = requests.post(API_URL, json=payload, timeout=120)
            latency = time.time() - start
            if resp.status_code != 200:
                st.error(f"API error {resp.status_code}: {resp.text}")
            else:
                data = resp.json()
                st.success(f"Generated in {latency:.2f} s (server reported {data.get('duration_seconds', 0):.2f} s)")
                st.subheader("Generated text")
                st.markdown(data.get("generated_text", ""))
                with st.expander("Show metadata"):
                    st.json(data)
                st.markdown("### cURL (for reproducibility)")
                st.code(
                    f"curl -X POST '{API_URL}' -H 'Content-Type: application/json' -d '{resp.request.body.decode() if hasattr(resp.request, \"body\") and resp.request.body else payload}'",
                    language="bash",
                )
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
