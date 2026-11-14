from typing import List, Optional
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="Structured Movie Extractor",
    page_icon="🎬",
    layout="wide",
)

# Custom CSS for clean cards and genre/cast pills
st.markdown(
    """
    <style>
    .summary-box {
        background-color: rgba(128, 128, 128, 0.08);
        border-left: 4px solid #ff4b4b;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .badge {
        display: inline-block;
        background-color: rgba(255, 75, 75, 0.14);
        color: #ff4b4b;
        border: 1px solid rgba(255, 75, 75, 0.35);
        border-radius: 999px;
        padding: 4px 12px;
        margin: 4px 6px 4px 0;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .cast-pill {
        display: inline-block;
        background-color: rgba(128, 128, 128, 0.12);
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 8px;
        padding: 6px 12px;
        margin: 4px 6px 4px 0;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 2. Pydantic Schema (Updated with default=None for Optional fields)
class Movie(BaseModel):
    title: str = Field(description="The official title of the movie.")
    release_year: Optional[int] = Field(
        default=None, description="The release year of the movie."
    )
    genre: List[str] = Field(
        default_factory=list, description="List of movie genres."
    )
    director: Optional[str] = Field(
        default=None, description="Director of the movie."
    )
    cast: List[str] = Field(
        default_factory=list, description="Main cast members."
    )
    music_credits: Optional[str] = Field(
        default=None, description="Music composer or soundtrack credits."
    )
    ratings: Optional[float] = Field(
        default=None, description="Numerical rating (e.g. IMDb score)."
    )
    summary: str = Field(
        description="A concise 1-2 sentence summary of the paragraph."
    )


# 3. Setup Parser & Prompt Template
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Extract Movie information strictly from the provided paragraph. "
        "Do not invent missing details.\n{format_instructions}",
    ),
    ("human", "{paragraph}"),
])

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

# 4. Sidebar Controls
with st.sidebar:
    st.title("⚙️ Extractor Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="0.0 keeps extraction strictly factual and JSON-safe.",
    )
    with st.expander("🔍 View Pydantic JSON Schema"):
        st.code(parser.get_format_instructions(), language="text")

# 5. Main Header
st.title("🎬 Structured Movie Information Extractor")
st.caption(
    "Powered by LangChain `PydanticOutputParser` & Groq • Validated Structured Output"
)
st.divider()

if "paragraph_text" not in st.session_state:
    st.session_state.paragraph_text = ""

# 6. Two-Column Workspace
left_col, right_col = st.columns([1, 1.15], gap="large")

with left_col:
    st.subheader("📄 Input Paragraph")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("✨ Load Sample Text", use_container_width=True):
            st.session_state.paragraph_text = SAMPLE_PARAGRAPH
            st.rerun()
    with b2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.paragraph_text = ""
            st.rerun()

    para = st.text_area(
        "Movie Paragraph",
        key="paragraph_text",
        height=270,
        placeholder="Paste a paragraph describing a movie...",
        label_visibility="collapsed",
    )

    run_btn = st.button(
        "🚀 Extract & Validate Data",
        type="primary",
        use_container_width=True,
    )

with right_col:
    st.subheader("📊 Validated Output")

    if run_btn:
        if not para.strip():
            st.warning("Please enter a paragraph or load the sample text first.")
        else:
            with st.spinner("Extracting & validating against Movie schema..."):
                try:
                    model = ChatGroq(
                        model="openai/gpt-oss-20b",
                        temperature=temperature,
                    )

                    # Full LCEL Chain: Prompt -> Model -> PydanticOutputParser
                    chain = prompt | model | parser
                    movie: Movie = chain.invoke({
                        "paragraph": para,
                        "format_instructions": parser.get_format_instructions(),
                    })

                    # Tabbed view: Visual UI Cards vs Raw Validated JSON
                    tab_ui, tab_json = st.tabs(
                        ["✨ Structured View", "🧾 Validated JSON"]
                    )

                    with tab_ui:
                        st.markdown(f"## 🎥 {movie.title}")

                        # Genre badges
                        if movie.genre:
                            badges_html = "".join(
                                f'<span class="badge">{g}</span>'
                                for g in movie.genre
                            )
                            st.markdown(badges_html, unsafe_allow_html=True)

                        st.write("")

                        # Key Metrics Row
                        m1, m2, m3 = st.columns(3)
                        m1.metric(
                            "📅 Release Year",
                            movie.release_year if movie.release_year else "N/A",
                        )
                        m2.metric(
                            "⭐ Rating",
                            f"{movie.ratings}/10" if movie.ratings else "N/A",
                        )
                        m3.metric(
                            "🎬 Director",
                            movie.director if movie.director else "N/A",
                        )

                        st.divider()

                        # Summary Box
                        st.markdown("**📝 Quick Summary**")
                        st.markdown(
                            f'<div class="summary-box">{movie.summary}</div>',
                            unsafe_allow_html=True,
                        )

                        # Music Credits
                        st.markdown(
                            f"**🎵 Music Credits:** {movie.music_credits or 'Not mentioned'}"
                        )

                        # Cast Pills
                        st.markdown("**🎭 Cast**")
                        if movie.cast:
                            cast_html = "".join(
                                f'<span class="cast-pill">👤 {actor}</span>'
                                for actor in movie.cast
                            )
                            st.markdown(cast_html, unsafe_allow_html=True)
                        else:
                            st.caption("No cast members mentioned.")

                    with tab_json:
                        json_output = movie.model_dump_json(indent=2)
                        st.code(json_output, language="json")
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=json_output,
                            file_name=f"{movie.title.lower().replace(' ', '_')}.json",
                            mime="application/json",
                            use_container_width=True,
                        )

                except Exception as e:
                    st.error(f"Extraction or Pydantic Validation Error: {e}")
    else:
        st.info(
            "Click **Extract & Validate Data** to parse the paragraph into a validated `Movie` object."
        )