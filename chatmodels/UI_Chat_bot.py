import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# Load environment variables (GROQ_API_KEY)
load_dotenv()

# 1. Page Configuration
st.set_page_config(page_title="Mood AI Agent", page_icon="🤖", layout="centered")

# Custom CSS for a cleaner look
st.markdown(
    """
    <style>
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Define AI Personalities
MODES = {
    "😠 Angry Mode": {
        "prompt": (
            "You are an angry AI agent. You respond aggressively and"
            " impatiently."
        ),
        "avatar": "😠",
        "desc": "Short-tempered, impatient, and aggressively honest.",
    },
    "😂 Funny Mode": {
        "prompt": "You are a Funny AI agent. You respond with humor and jokes.",
        "avatar": "😂",
        "desc": "Cracks jokes, uses sarcasm, and keeps things lighthearted.",
    },
    "😢 Sad Mode": {
        "prompt": "You are a SAD AI agent. You respond and sound depressed.",
        "avatar": "😢",
        "desc": "Gloomy, pessimistic, and sighs at every prompt.",
    },
}

# 3. Sidebar Controls
with st.sidebar:
    st.title("⚙️ Agent Settings")

    selected_mode = st.selectbox(
        "Choose your AI Agent:",
        options=list(MODES.keys()),
        index=1,  # Default to Funny Mode
    )

    st.info(MODES[selected_mode]["desc"])

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.1,
        help="Closer to 0 = logical/focused. Closer to 1 = creative/random.",
    )

    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            SystemMessage(content=MODES[selected_mode]["prompt"])
        ]
        st.rerun()

# 4. Initialize or Reset Session State when Mode Changes
if "current_mode" not in st.session_state:
    st.session_state.current_mode = selected_mode

if (
    "messages" not in st.session_state
    or st.session_state.current_mode != selected_mode
):
    st.session_state.current_mode = selected_mode
    st.session_state.messages = [
        SystemMessage(content=MODES[selected_mode]["prompt"])
    ]

# 5. Main Chat Header
st.title(f"{selected_mode} Chat")
st.caption("Powered by Groq & LangChain")
st.divider()

# 6. Display Chat History (Skipping the hidden SystemMessage)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🧑"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar=MODES[selected_mode]["avatar"]):
            st.markdown(msg.content)

# 7. Handle User Input
if prompt := st.chat_input("Say something to the AI..."):
    # Display and save user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # Initialize model with current slider temperature
    model = ChatGroq(model="openai/gpt-oss-20b", temperature=temperature)

    # Generate and display AI response
    with st.chat_message("assistant", avatar=MODES[selected_mode]["avatar"]):
        with st.spinner("Thinking..."):
            try:
                response = model.invoke(st.session_state.messages)
                st.markdown(response.content)
                st.session_state.messages.append(
                    AIMessage(content=response.content)
                )
            except Exception as e:
                st.error(f"Error communicating with Groq: {e}")