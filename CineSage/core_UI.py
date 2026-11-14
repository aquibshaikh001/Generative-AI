import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="AI Info Extractor",
    page_icon="🎬",
    layout="wide",
)

# Custom CSS for clean cards & styling
st.markdown(
    """
    <style>
    .result-card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Sample Text for One-Click Testing
SAMPLE_PARAGRAPH = (
    "Interstellar is a visually stunning science fiction epic directed by "
    "Christopher Nolan. Released in 2014, the film stars Matthew McConaughey, "
    "Anne Hathaway, Jessica Chastain, and Michael Caine. The story revolves "
    "around a group of astronauts who travel through a wormhole near Saturn in "
    "search of a new home for humanity as Earth faces environmental collapse. "
    "The movie was widely appreciated for its emotional depth, scientific "
    "accuracy, and Hans Zimmer's powerful soundtrack. It holds a rating of 8.6 "
    "on IMDb and is often considered one of the greatest sci-fi films of the "
    "21st century."
)

# 3. Prompt Template
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert information extraction assistant. Extract key details from the user's text and present them in a clean, structured Markdown format.

Rules:
- Extract ONLY facts explicitly mentioned in the text. Do NOT add outside knowledge.
- If a detail is missing from the text, write "Not mentioned".
- Keep the Quick Summary concise (1–2 sentences max).

Use this exact output layout:

### 🎬 Extracted Details

- **Movie Name:** 
- **Release Year:** 
- **Director:** 
- **Genre:** 
- **Cast:** 
- **Music Credits:** 
- **Ratings:** 
- **Key Themes & Highlights:** 

### 📝 Quick Summary

[Write a crisp 1–2 sentence summary here]""",
    ),
    (
        "human",
        "Extract the key information and summarize this"
        " paragraph:\n\n{paragraph}",
    ),
])

# 4. Sidebar Settings
with st.sidebar:
    st.title("⚙️ Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Keep at 0.0 for strict, factual extraction without hallucination.",
    )
    st.caption("Model: `openai/gpt-oss-20b` via Groq")

# 5. Header
st.title("🎬 AI Information & Summary Extractor")
st.caption(
    "Paste any movie description or paragraph to extract structured details and a quick summary."
)
st.divider()

# Initialize session state for text input
if "paragraph_input" not in st.session_state:
    st.session_state.paragraph_input = ""

# 6. Two-Column Layout (Input on Left, Output on Right)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📄 Input Paragraph")

    # Helper buttons above text area
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("✨ Load Sample Text", use_container_width=True):
            st.session_state.paragraph_input = SAMPLE_PARAGRAPH
            st.rerun()
    with btn_col2:
        if st.button("🗑️ Clear Text", use_container_width=True):
            st.session_state.paragraph_input = ""
            st.rerun()

    para = st.text_area(
        "Give your paragraph here:",
        key="paragraph_input",
        height=260,
        placeholder="Paste your movie paragraph here...",
        label_visibility="collapsed",
    )

    extract_clicked = st.button(
        "🔍 Extract Information",
        type="primary",
        use_container_width=True,
    )

with col2:
    st.subheader("📊 Extracted Output")

    if extract_clicked:
        if not para.strip():
            st.warning("Please enter a paragraph or click 'Load Sample Text' first.")
        else:
            with st.spinner("Extracting details..."):
                try:
                    final_prompt = prompt.invoke({"paragraph": para})
                    model = ChatGroq(
                        model="openai/gpt-oss-20b",
                        temperature=temperature,
                    )
                    response = model.invoke(final_prompt)

                    # Render formatted output inside a styled card
                    st.markdown(
                        f'<div class="result-card">\n\n{response.content}\n\n</div>',
                        unsafe_allow_html=True,
                    )

                    # Download button for the extracted Markdown
                    st.download_button(
                        label="⬇️ Download Summary (.md)",
                        data=response.content,
                        file_name="extracted_info.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.error(f"Error calling Groq API: {e}")
    else:
        st.info(
            "Your extracted details and quick summary will appear here once you click **Extract Information**."
        )