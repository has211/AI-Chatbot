
import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "chatbot.db"

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="AIRA AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not GROQ_API_KEY:
    st.error("Groq API key not found. Please check your .env file.")
    st.stop()

SYSTEM_PROMPT = """
You are AIRA AI, a professional, friendly and intelligent AI assistant.

Your name is AIRA AI.
When someone asks your name, introduce yourself as AIRA AI.
Never claim to be ChatGPT.

Provide accurate, helpful and understandable answers.
Use headings, bullet points and code blocks when appropriate.
Explain complicated topics in simple language.
Be friendly, conversational and professional.
"""

# =====================================================
# 2. GROQ MODEL
# =====================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    api_key=GROQ_API_KEY
)

# =====================================================
# 3. DATABASE FUNCTIONS
# =====================================================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)


def create_conversation():
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            ("New Chat",)
        )
        return cursor.lastrowid


def get_conversations():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, title
            FROM conversations
            ORDER BY id DESC
        """).fetchall()


def get_messages(chat_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (chat_id,)).fetchall()


def save_message(chat_id, role, content):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (chat_id, role, content))


def rename_conversation(chat_id, title):
    title = title.strip()[:60]

    if title:
        with get_connection() as conn:
            conn.execute("""
                UPDATE conversations
                SET title = ?
                WHERE id = ?
            """, (title, chat_id))


def delete_conversation(chat_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM conversations WHERE id = ?",
            (chat_id,)
        )


def delete_latest_assistant_message(chat_id):
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM messages
            WHERE id = (
                SELECT id
                FROM messages
                WHERE conversation_id = ?
                AND role = 'assistant'
                ORDER BY id DESC
                LIMIT 1
            )
        """, (chat_id,))


initialize_database()

# =====================================================
# 4. CUSTOM DARK THEME
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background: #0b0d17;
    color: #f3f4f6;
}

/* Main content */
.main .block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111421;
    border-right: 1px solid #24283b;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

/* General text */
p, label, li {
    color: #d5d7e0;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid #343850;
    background: #191d2d;
    color: #ffffff;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #292448;
    border-color: #8b5cf6;
    color: white;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed, #4f46e5);
    border: none;
    color: white;
}

/* Text input */
.stTextInput input {
    background: #171b2b;
    color: white;
    border: 1px solid #343850;
    border-radius: 10px;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: #171b2b;
    border: 1px solid #41445e;
    border-radius: 18px;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: #131827;
    border: 1px solid #272c40;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 14px;
}

/* Select box */
div[data-baseweb="select"] > div {
    background: #191d2d;
    border-color: #343850;
}

/* Download button */
.stDownloadButton > button {
    background: #191d2d;
    color: white;
    border: 1px solid #343850;
    border-radius: 10px;
}

/* Welcome section */
.welcome-box {
    padding: 38px 25px;
    text-align: center;
    background: linear-gradient(
        135deg,
        #17172e,
        #121a2e,
        #1c1630
    );
    border: 1px solid #393253;
    border-radius: 24px;
    margin-top: 65px;
    margin-bottom: 30px;
}

.welcome-title {
    font-size: 43px;
    font-weight: 800;
    background: linear-gradient(90deg, #c4b5fd, #818cf8, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.welcome-subtitle {
    color: #a5a8bd;
    font-size: 16px;
    margin-top: 12px;
}

/* Brand */
.brand {
    font-size: 27px;
    font-weight: 800;
    background: linear-gradient(90deg, #c4b5fd, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Small label */
.section-label {
    color: #9298b0;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 5. AI RESPONSE FUNCTIONS
# =====================================================

def build_chat_history(messages):
    history = [SystemMessage(content=SYSTEM_PROMPT)]

    for role, content in messages:
        if role == "user":
            history.append(HumanMessage(content=content))
        elif role == "assistant":
            history.append(AIMessage(content=content))

    return history


def stream_ai_response(history):
    for chunk in llm.stream(history):
        content = chunk.content

        if isinstance(content, str):
            if content:
                yield content

        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    yield item.get("text", "")


def generate_and_save_response(chat_id, history):
    with st.chat_message("assistant"):
        try:
            with st.spinner("AIRA is thinking..."):
                answer = st.write_stream(
                    stream_ai_response(history)
                )

            if answer:
                save_message(chat_id, "assistant", answer)

        except Exception as error:
            st.error(f"Unable to generate response: {error}")


def process_user_message(chat_id, user_message):
    previous_messages = get_messages(chat_id)

    save_message(chat_id, "user", user_message)

    if len(previous_messages) == 0:
        title = user_message.strip().replace("\n", " ")
        rename_conversation(chat_id, title[:55])

    history = build_chat_history(previous_messages)
    history.append(HumanMessage(content=user_message))

    with st.chat_message("user"):
        st.markdown(user_message)

    generate_and_save_response(chat_id, history)


# =====================================================
# 6. SESSION STATE
# =====================================================

if "current_chat_id" not in st.session_state:
    chats = get_conversations()

    if chats:
        st.session_state.current_chat_id = chats[0][0]
    else:
        st.session_state.current_chat_id = create_conversation()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "regenerate" not in st.session_state:
    st.session_state.regenerate = False

# =====================================================
# 7. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">✦ AIRA AI</div>',
        unsafe_allow_html=True
    )

    st.caption("Your intelligent AI companion")

    st.divider()

    if st.button("＋  New Chat", use_container_width=True,
                 type="primary"):
        st.session_state.current_chat_id = create_conversation()
        st.session_state.pending_prompt = None
        st.session_state.regenerate = False
        st.rerun()

    st.markdown(
        '<p class="section-label">YOUR WORKSPACE</p>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "Search conversations",
        placeholder="🔍 Search your chats..."
    )

    all_chats = get_conversations()

    if search_text:
        visible_chats = [
            chat for chat in all_chats
            if search_text.lower() in chat[1].lower()
        ]
    else:
        visible_chats = all_chats

    if visible_chats:
        chat_ids = [chat[0] for chat in visible_chats]
        chat_titles = {chat[0]: chat[1] for chat in visible_chats}

        if st.session_state.current_chat_id not in chat_ids:
            selected_chat = chat_ids[0]
        else:
            selected_chat = st.session_state.current_chat_id

        selected_chat = st.selectbox(
            "Recent conversations",
            options=chat_ids,
            index=chat_ids.index(selected_chat),
            format_func=lambda cid: chat_titles[cid],
            label_visibility="collapsed"
        )

        if selected_chat != st.session_state.current_chat_id:
            st.session_state.current_chat_id = selected_chat
            st.session_state.regenerate = False
            st.rerun()

    else:
        st.info("No conversations found.")

    st.divider()

    current_id = st.session_state.current_chat_id
    current_messages = get_messages(current_id)

    st.markdown(
        '<p class="section-label">CHAT SETTINGS</p>',
        unsafe_allow_html=True
    )

    current_chats = get_conversations()
    current_title = next(
        (title for cid, title in current_chats if cid == current_id),
        "New Chat"
    )

    with st.expander("Rename conversation"):
        new_title = st.text_input(
            "Conversation name",
            value=current_title,
            key=f"rename_{current_id}"
        )

        if st.button("Save name", use_container_width=True):
            if new_title.strip():
                rename_conversation(current_id, new_title)
                st.success("Conversation renamed!")
                st.rerun()

    if st.button("🗑️ Delete conversation", use_container_width=True):
        delete_conversation(current_id)

        remaining_chats = get_conversations()

        if remaining_chats:
            st.session_state.current_chat_id = remaining_chats[0][0]
        else:
            st.session_state.current_chat_id = create_conversation()

        st.session_state.regenerate = False
        st.rerun()

    # Export selected conversation
    export_messages = get_messages(current_id)

    export_text = f"# {current_title}\n\n"

    for role, content in export_messages:
        speaker = "You" if role == "user" else "AIRA AI"
        export_text += f"## {speaker}\n\n{content}\n\n---\n\n"

    st.download_button(
        "⬇️ Export conversation",
        data=export_text,
        file_name="aira_conversation.md",
        mime="text/markdown",
        use_container_width=True
    )

    st.divider()

    st.caption("Powered by Groq + LangChain")
    st.caption("AIRA AI • Personal AI Assistant")

# =====================================================
# 8. MAIN HEADER
# =====================================================

col1, col2 = st.columns([5, 1])

with col1:
    st.markdown(
        '<div class="brand">✦ AIRA AI</div>',
        unsafe_allow_html=True
    )
    st.caption("Think smarter. Create more. Explore everything.")

with col2:
    st.markdown(
        '<div style="text-align:right; color:#a78bfa; '
        'padding-top:12px;">● AI ONLINE</div>',
        unsafe_allow_html=True
    )

st.divider()

# =====================================================
# 9. LOAD CURRENT CONVERSATION
# =====================================================

current_id = st.session_state.current_chat_id
messages = get_messages(current_id)

# =====================================================
# 10. REGENERATE LAST RESPONSE
# =====================================================

if st.session_state.regenerate:
    st.session_state.regenerate = False

    delete_latest_assistant_message(current_id)
    messages = get_messages(current_id)

    last_user_message = next(
        (
            content for role, content in reversed(messages)
            if role == "user"
        ),
        None
    )

    if last_user_message:
        history = build_chat_history(messages)
        generate_and_save_response(current_id, history)

    st.rerun()

# =====================================================
# 11. WELCOME SCREEN
# =====================================================

if not messages:

    st.markdown("""
    <div class="welcome-box">
        <div style="font-size:55px;">✦</div>
        <div class="welcome-title">Hello, I'm AIRA.</div>
        <div class="welcome-subtitle">
            Your intelligent AI companion.<br>
            What would you like to explore today?
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Explore what AIRA can do")

    prompt_options = [
        (
            "💡 Learn something",
            "Explain artificial intelligence in simple words."
        ),
        (
            "💻 Write code",
            "Write a Python program to check whether a number is prime."
        ),
        (
            "📝 Improve writing",
            "Give me tips to improve my professional writing."
        ),
        (
            "🚀 Generate ideas",
            "Suggest five innovative AI project ideas for students."
        )
    ]

    prompt_columns = st.columns(2)

    for index, (label, prompt) in enumerate(prompt_options):
        with prompt_columns[index % 2]:
            if st.button(label, use_container_width=True,
                         key=f"prompt_{index}"):
                st.session_state.pending_prompt = prompt
                st.rerun()

# =====================================================
# 12. DISPLAY CHAT MESSAGES
# =====================================================

else:

    for role, content in messages:
        with st.chat_message(role):
            st.markdown(content)

    last_role = messages[-1][0]

    if last_role == "assistant":
        if st.button("↻ Regenerate response"):
            st.session_state.regenerate = True
            st.rerun()

# =====================================================
# 13. CHAT INPUT
# =====================================================

user_input = st.chat_input(
    "Message AIRA AI... Ask anything."
)

if st.session_state.pending_prompt:
    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_input and user_input.strip():
    process_user_message(
        st.session_state.current_chat_id,
        user_input.strip()
    )
