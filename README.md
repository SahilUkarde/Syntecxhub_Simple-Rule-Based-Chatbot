# Syntecxhub_Simple-Rule-Based-Chatbot

A console-based conversational chatbot built using **pattern matching (regex)**.
It supports common intents like greetings, help, small talk, and answers
domain-specific questions using a built-in knowledge base. All conversations
are logged to a text file with timestamps.

## Features

- **Intent recognition** via regex pattern matching
  - Greeting, goodbye, thanks, help, how-are-you, name introduction, weather/mood small talk
- **Knowledge base** for domain questions (e.g., "What is Python?", "What is AI?", "What is the capital of France?")
- **Randomized responses** for a more natural feel
- **Fallback responses** when input isn't understood
- **Conversation logging** to `conversation_log.txt` with timestamps

## Project Structure

```
.
├── chatbot.py            # Main chatbot application
├── conversation_log.txt  # Auto-generated log of conversations (created on run)
└── README.md
```

## Requirements

- Python 3.6+
- No external libraries needed (uses only `re`, `random`, `datetime`)

## How to Run

```bash
python chatbot.py
```

Then start chatting in the console:

```
You: hi
Bot: Hello! How can I help you today?

You: what is python
Bot: Python is a high-level, interpreted programming language known for its readability and versatility.

You: my name is Alex
Bot: Nice to meet you, Alex!

You: bye
Bot: Goodbye! Have a great day!
```

Type `bye`, `exit`, or `quit` to end the conversation.

## How It Works

1. **Knowledge Base Check** — The bot first checks if the user's message
   matches a question in `KNOWLEDGE_BASE` (a dictionary of Q&A pairs).
2. **Intent Matching** — If no knowledge-base match is found, the bot checks
   the input against a list of regex patterns grouped by intent
   (`INTENTS`), each with a set of possible responses.
3. **Fallback** — If nothing matches, the bot responds with a randomized
   "I didn't understand" message.
4. **Logging** — Every user message and bot response is appended to
   `conversation_log.txt` with a timestamp.

## Extending the Bot

- Add more entries to `KNOWLEDGE_BASE` for additional domain questions.
- Add new intents to `INTENTS` with their own regex patterns and responses.
- Swap regex matching for fuzzy matching (`difflib`) to handle typos.
- Integrate with **ChatterBot** or **AIML** for more advanced, trainable
  conversation handling.

## License

This project is open source and available for personal or educational use.
