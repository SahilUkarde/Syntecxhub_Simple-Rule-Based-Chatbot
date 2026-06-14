"""
Simple Rule-Based Chatbot
==========================
A console chatbot that uses regex pattern matching to detect intents
(greeting, help, small talk, knowledge-base queries, goodbye) and
responds with rule-based replies. Every conversation turn is logged
to a text file with a timestamp.

Run:
    python chatbot.py
"""

import re
import random
from datetime import datetime


# ---------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------
# A small dictionary of domain questions -> answers.
# Keys are normalized (lowercase) keywords/phrases found in user input.
KNOWLEDGE_BASE = {
    "what is python": "Python is a high-level, interpreted programming "
                       "language known for its readability and versatility.",
    "who created python": "Python was created by Guido van Rossum and "
                           "first released in 1991.",
    "what is ai": "AI (Artificial Intelligence) refers to systems that can "
                   "perform tasks that normally require human intelligence, "
                   "such as reasoning, learning, and problem solving.",
    "what is machine learning": "Machine Learning is a subset of AI where "
                                 "systems learn patterns from data instead "
                                 "of being explicitly programmed.",
    "what is a chatbot": "A chatbot is a software application that simulates "
                          "human conversation through text or voice.",
    "what is nlp": "NLP (Natural Language Processing) is a field of AI that "
                    "focuses on enabling computers to understand and generate "
                    "human language.",
    "what is the capital of india": "The capital of India is New Delhi.",
    "what is the capital of france": "The capital of France is Paris.",
}


# ---------------------------------------------------------------------
# Intent Patterns
# ---------------------------------------------------------------------
# Each intent maps to a list of regex patterns and a list of possible
# responses. Patterns are checked in order, and the first match wins.
INTENTS = [
    {
        "intent": "greeting",
        "patterns": [
            r"\b(hi|hello|hey|hola|good morning|good evening|good afternoon)\b"
        ],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! What would you like to talk about?",
            "Hey! Good to see you. Ask me anything.",
        ],
    },
    {
        "intent": "goodbye",
        "patterns": [
            r"\b(bye|goodbye|see you|exit|quit|farewell)\b"
        ],
        "responses": [
            "Goodbye! Have a great day!",
            "See you later! Take care.",
            "Bye! Feel free to come back anytime.",
        ],
    },
    {
        "intent": "thanks",
        "patterns": [
            r"\b(thanks|thank you|thx|appreciate it)\b"
        ],
        "responses": [
            "You're welcome!",
            "Anytime! Happy to help.",
            "No problem at all!",
        ],
    },
    {
        "intent": "help",
        "patterns": [
            r"\b(help|what can you do|options|menu|commands)\b"
        ],
        "responses": [
            "I can chat with you, answer simple knowledge questions "
            "(try asking 'what is python' or 'what is AI'), and respond "
            "to greetings and small talk. Type 'bye' to exit.",
        ],
    },
    {
        "intent": "how_are_you",
        "patterns": [
            r"\b(how are you|how's it going|how do you do|how are things)\b"
        ],
        "responses": [
            "I'm just a program, but I'm running smoothly! How about you?",
            "Doing great, thanks for asking! How can I assist you?",
        ],
    },
    {
        "intent": "name",
        "patterns": [
            r"\b(your name|who are you|what are you called)\b"
        ],
        "responses": [
            "I'm a simple rule-based chatbot, created to chat and answer "
            "basic questions.",
        ],
    },
    {
        "intent": "user_name",
        "patterns": [
            r"\bmy name is (\w+)\b",
            r"\bi am (\w+)\b",
            r"\bi'm (\w+)\b",
        ],
        "responses": [
            "Nice to meet you, {0}!",
            "Hello, {0}! Great to have you here.",
        ],
    },
    {
        "intent": "weather_smalltalk",
        "patterns": [
            r"\b(weather|raining|sunny|cold|hot)\b"
        ],
        "responses": [
            "I can't check live weather, but I hope it's pleasant where you are!",
        ],
    },
    {
        "intent": "small_talk_mood",
        "patterns": [
            r"\b(i am (sad|happy|tired|bored|excited|angry))\b",
            r"\b(i'm (sad|happy|tired|bored|excited|angry))\b",
        ],
        "responses": [
            "I see — thanks for sharing that with me. Want to talk about it?",
            "Got it. I'm here if you want to chat more about it.",
        ],
    },
]


# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------
LOG_FILE = "conversation_log.txt"


def log_message(speaker, message):
    """Append a single conversation turn to the log file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {speaker}: {message}\n")


# ---------------------------------------------------------------------
# Core Logic
# ---------------------------------------------------------------------
def check_knowledge_base(user_input):
    """Return a knowledge-base answer if the user's question matches a key."""
    text = user_input.lower().strip("?!. ")
    # Direct match
    if text in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[text]
    # Partial match: check if any KB key phrase appears in the input
    for key, answer in KNOWLEDGE_BASE.items():
        if key in text:
            return answer
    return None


def match_intent(user_input):
    """Try to match the user input against known intent patterns."""
    text = user_input.lower()
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            match = re.search(pattern, text)
            if match:
                response = random.choice(intent["responses"])
                if match.groups():
                    # Fill in captured groups (e.g., user's name), capitalized
                    groups = [g.capitalize() for g in match.groups()]
                    response = response.format(*groups)
                return intent["intent"], response
    return None, None


def get_response(user_input):
    """Generate a bot response: try knowledge base first, then intents."""
    if not user_input.strip():
        return "I didn't catch that. Could you say something?"

    # 1. Knowledge base lookup (domain questions)
    kb_answer = check_knowledge_base(user_input)
    if kb_answer:
        return kb_answer

    # 2. Intent-based pattern matching
    intent, response = match_intent(user_input)
    if response:
        return response

    # 3. Fallback
    fallback_responses = [
        "I'm not sure I understand. Could you rephrase that?",
        "Hmm, I don't have an answer for that yet. Try asking about "
        "Python, AI, or just say hello!",
        "Sorry, I didn't get that. Type 'help' to see what I can do.",
    ]
    return random.choice(fallback_responses)


# ---------------------------------------------------------------------
# Main Interactive Loop
# ---------------------------------------------------------------------
def main():
    print("=" * 60)
    print(" Simple Rule-Based Chatbot ".center(60, "="))
    print("=" * 60)
    print("Type 'bye', 'exit', or 'quit' to end the conversation.")
    print("Type 'help' to see what I can do.\n")

    log_message("SYSTEM", "Conversation started")

    while True:
        user_input = input("You: ").strip()
        log_message("User", user_input)

        response = get_response(user_input)
        print(f"Bot: {response}")
        log_message("Bot", response)

        if re.search(r"\b(bye|goodbye|see you|exit|quit|farewell)\b",
                      user_input.lower()):
            log_message("SYSTEM", "Conversation ended")
            break


if __name__ == "__main__":
    main()
