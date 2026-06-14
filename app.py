"""
Streamlit Web App — Simple Rule-Based Chatbot
=============================================
Run locally:
    pip install streamlit
    streamlit run app.py

Then share via:
    streamlit run app.py   (local)
    Upload to https://share.streamlit.io for a public shareable link.
"""

import re
import random
from datetime import datetime
import streamlit as st

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Rule-Based Chatbot",
    page_icon="🤖",
    layout="centered",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Header ── */
.chat-header {
    text-align: center;
    padding: 2rem 0 1.2rem;
}
.chat-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.chat-header p {
    color: #a78bfa;
    font-size: 0.9rem;
    margin: 0.4rem 0 0;
}

/* ── Chat container ── */
.chat-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    max-height: 460px;
    overflow-y: auto;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* ── Message bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 0.85rem;
    align-items: flex-end;
    gap: 0.5rem;
}
.msg-row.user  { flex-direction: row-reverse; }
.msg-row.bot   { flex-direction: row; }

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.avatar.bot  { background: #7c3aed; }
.avatar.user { background: #0ea5e9; }

.bubble {
    max-width: 72%;
    padding: 0.65rem 1rem;
    border-radius: 14px;
    font-size: 0.88rem;
    line-height: 1.55;
    word-wrap: break-word;
}
.bubble.bot {
    background: rgba(124, 58, 237, 0.25);
    border: 1px solid rgba(124, 58, 237, 0.4);
    color: #e9d5ff;
    border-bottom-left-radius: 4px;
}
.bubble.user {
    background: rgba(14, 165, 233, 0.25);
    border: 1px solid rgba(14, 165, 233, 0.4);
    color: #bae6fd;
    border-bottom-right-radius: 4px;
}

.timestamp {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.3);
    margin-top: 2px;
    text-align: right;
}
.msg-row.bot .timestamp { text-align: left; }

/* ── Quick-reply chips ── */
.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 1rem;
}
.chip {
    background: rgba(124,58,237,0.2);
    border: 1px solid rgba(124,58,237,0.5);
    color: #c4b5fd;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.78rem;
    cursor: pointer;
    transition: background 0.2s;
}
.chip:hover { background: rgba(124,58,237,0.45); }

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    gap: 1.2rem;
    justify-content: center;
    margin-bottom: 1.2rem;
}
.stat {
    text-align: center;
}
.stat-num {
    font-size: 1.3rem;
    font-weight: 700;
    color: #a78bfa;
}
.stat-lbl {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Input overrides ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.35) !important; }
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Log expander ── */
.stExpander {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Knowledge Base
# ─────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "what is python": "Python is a high-level, interpreted programming language known for its readability and versatility.",
    "who created python": "Python was created by Guido van Rossum and first released in 1991.",
    "what is ai": "AI (Artificial Intelligence) refers to systems that perform tasks normally requiring human intelligence, such as reasoning, learning, and problem solving.",
    "what is machine learning": "Machine Learning is a subset of AI where systems learn patterns from data instead of being explicitly programmed.",
    "what is a chatbot": "A chatbot is a software application that simulates human conversation through text or voice.",
    "what is nlp": "NLP (Natural Language Processing) is a field of AI focused on enabling computers to understand and generate human language.",
    "what is deep learning": "Deep Learning is a subset of ML that uses multi-layered neural networks to model complex patterns in data.",
    "what is streamlit": "Streamlit is an open-source Python library that makes it easy to build and share beautiful web apps for machine learning and data science.",
    "what is github": "GitHub is a web-based platform for version control and collaboration, allowing developers to host and review code using Git.",
    "what is the capital of india": "The capital of India is New Delhi.",
    "what is the capital of france": "The capital of France is Paris.",
    "what is the capital of usa": "The capital of the USA is Washington, D.C.",
}

# ─────────────────────────────────────────────
# Intents
# ─────────────────────────────────────────────
INTENTS = [
    {
        "intent": "greeting",
        "patterns": [r"\b(hi|hello|hey|hola|good morning|good evening|good afternoon)\b"],
        "responses": [
            "Hello! 👋 How can I help you today?",
            "Hi there! What would you like to talk about?",
            "Hey! Great to see you. Ask me anything.",
        ],
    },
    {
        "intent": "goodbye",
        "patterns": [r"\b(bye|goodbye|see you|exit|quit|farewell)\b"],
        "responses": [
            "Goodbye! 👋 Have a great day!",
            "See you later! Take care. 😊",
            "Bye! Feel free to come back anytime.",
        ],
    },
    {
        "intent": "thanks",
        "patterns": [r"\b(thanks|thank you|thx|appreciate it)\b"],
        "responses": [
            "You're welcome! 😊",
            "Anytime! Happy to help.",
            "No problem at all! 🙌",
        ],
    },
    {
        "intent": "help",
        "patterns": [r"\b(help|what can you do|options|commands)\b"],
        "responses": [
            "I can answer questions about Python, AI, ML, NLP, Streamlit, GitHub, and more. "
            "Try asking 'What is Python?' or 'What is AI?'. I also enjoy small talk! 💬",
        ],
    },
    {
        "intent": "how_are_you",
        "patterns": [r"\b(how are you|how's it going|how do you do|how are things)\b"],
        "responses": [
            "I'm just a bot, but I'm running smoothly! How about you? 😄",
            "Doing great, thanks for asking! How can I assist you?",
        ],
    },
    {
        "intent": "name",
        "patterns": [r"\b(your name|who are you|what are you called)\b"],
        "responses": [
            "I'm a rule-based chatbot 🤖 built with Python and Streamlit!",
        ],
    },
    {
        "intent": "user_name",
        "patterns": [r"\bmy name is (\w+)\b", r"\bi am (\w+)\b", r"\bi'm (\w+)\b"],
        "responses": [
            "Nice to meet you, {0}! 🎉",
            "Hello, {0}! Great to have you here. 😊",
        ],
    },
    {
        "intent": "weather",
        "patterns": [r"\b(weather|raining|sunny|cold|hot)\b"],
        "responses": [
            "I can't check live weather ☁️, but I hope it's pleasant where you are!",
        ],
    },
    {
        "intent": "joke",
        "patterns": [r"\b(joke|funny|make me laugh|tell me a joke)\b"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄",
            "How many programmers does it take to change a light bulb? None — it's a hardware problem! 💡",
            "Why did the developer quit? Because they didn't get arrays! 😄",
        ],
    },
    {
        "intent": "creator",
        "patterns": [r"\b(who made you|who built you|who created you|your creator)\b"],
        "responses": [
            "I was built as a student project using Python, regex pattern matching, and Streamlit! 🚀",
        ],
    },
]

QUICK_REPLIES = [
    "What is Python?", "What is AI?", "Tell me a joke",
    "What is NLP?", "What is Streamlit?", "Who are you?",
]

# ─────────────────────────────────────────────
# Core logic
# ─────────────────────────────────────────────
def check_knowledge_base(text):
    t = text.lower().strip("?!. ")
    if t in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[t]
    for key, answer in KNOWLEDGE_BASE.items():
        if key in t:
            return answer
    return None

def match_intent(text):
    t = text.lower()
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            m = re.search(pattern, t)
            if m:
                response = random.choice(intent["responses"])
                if m.groups():
                    response = response.format(*[g.capitalize() for g in m.groups()])
                return response
    return None

FALLBACKS = [
    "I'm not sure I understand. Could you rephrase that? 🤔",
    "Hmm, try asking about Python, AI, or just say hello!",
    "I didn't get that. Type **help** to see what I can do.",
]

def get_response(user_input):
    if not user_input.strip():
        return "I didn't catch that. Could you say something?"
    kb = check_knowledge_base(user_input)
    if kb:
        return kb
    intent_resp = match_intent(user_input)
    if intent_resp:
        return intent_resp
    return random.choice(FALLBACKS)

# ─────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.log = []
    st.session_state.user_count = 0
    st.session_state.bot_count = 0

def add_message(role, text):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": role, "text": text, "time": ts})
    st.session_state.log.append(f"[{ts}] {role.upper()}: {text}")
    if role == "user":
        st.session_state.user_count += 1
    else:
        st.session_state.bot_count += 1

# ─────────────────────────────────────────────
# Welcome message
# ─────────────────────────────────────────────
if not st.session_state.messages:
    add_message("bot", "Hello! 👋 I'm your rule-based chatbot. Ask me about Python, AI, ML, NLP, or just say hi!")

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <h1>🤖 Rule-Based Chatbot</h1>
    <p>Pattern matching · Knowledge base · Real-time responses</p>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown(f"""
<div class="stats-bar">
    <div class="stat"><div class="stat-num">{len(st.session_state.messages)}</div><div class="stat-lbl">Messages</div></div>
    <div class="stat"><div class="stat-num">{st.session_state.user_count}</div><div class="stat-lbl">From You</div></div>
    <div class="stat"><div class="stat-num">{st.session_state.bot_count}</div><div class="stat-lbl">Bot Replies</div></div>
    <div class="stat"><div class="stat-num">{len(KNOWLEDGE_BASE)}</div><div class="stat-lbl">KB Entries</div></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Chat window
# ─────────────────────────────────────────────
chat_html = '<div class="chat-box">'
for msg in st.session_state.messages:
    role = msg["role"]
    avatar = "🤖" if role == "bot" else "🧑"
    chat_html += f"""
    <div class="msg-row {role}">
        <div class="avatar {role}">{avatar}</div>
        <div>
            <div class="bubble {role}">{msg["text"]}</div>
            <div class="timestamp">{msg["time"]}</div>
        </div>
    </div>"""
chat_html += "</div>"
st.markdown(chat_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Quick reply chips
# ─────────────────────────────────────────────
st.markdown('<div class="chip-row">' +
    "".join(f'<span class="chip">{q}</span>' for q in QUICK_REPLIES) +
    "</div>", unsafe_allow_html=True)

cols = st.columns(len(QUICK_REPLIES))
for i, qr in enumerate(QUICK_REPLIES):
    if cols[i].button(qr, key=f"qr_{i}", use_container_width=True):
        add_message("user", qr)
        add_message("bot", get_response(qr))
        st.rerun()

# ─────────────────────────────────────────────
# Input area
# ─────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your message here…", key="input", label_visibility="collapsed")
with col2:
    send = st.button("Send 🚀", use_container_width=True)

if send and user_input.strip():
    add_message("user", user_input.strip())
    add_message("bot", get_response(user_input.strip()))
    st.rerun()

# ─────────────────────────────────────────────
# Conversation Log
# ─────────────────────────────────────────────
with st.expander("📋 View Conversation Log"):
    if st.session_state.log:
        st.code("\n".join(st.session_state.log), language="text")
    else:
        st.info("No conversation yet.")

col_a, col_b = st.columns(2)
with col_a:
    if st.session_state.log:
        st.download_button(
            "⬇️ Download Log",
            "\n".join(st.session_state.log),
            file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
with col_b:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.log = []
        st.session_state.user_count = 0
        st.session_state.bot_count = 0
        add_message("bot", "Chat cleared! Start a fresh conversation. 👋")
        st.rerun()
