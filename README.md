# 🔎 Personal AI Research Assistant

A Python-based AI research assistant that searches the web for relevant sources and uses an LLM to synthesize the retrieved information into a concise, source-referenced answer.

This project is part of my journey toward building practical AI engineering systems, focusing on **research workflows, information retrieval, and LLM integration**.

---

## 🎯 Project Goal

The goal of this project is to build a simple AI-powered research pipeline:

```text
Question
   ↓
Web Search
   ↓
Retrieve Sources
   ↓
LLM
   ↓
Synthesis
   ↓
Summary + Sources
```

Instead of asking an LLM to answer a question purely from its existing knowledge, the application first retrieves information from the web and provides that information to the LLM as research context.

---

## 🚀 V1 Features

* Accepts a research question from the user
* Searches the web using Tavily
* Retrieves multiple relevant sources
* Extracts source titles, URLs, and content
* Passes retrieved information to an OpenAI model
* Generates a research summary
* Produces key points
* References sources using numbered citations
* Instructs the LLM to use only the retrieved sources
* Identifies conflicting information between sources

---

## 🧠 What I'm Learning

### Research

This project introduces the fundamentals of AI-assisted research:

* Information retrieval
* Web search
* Source collection
* Working with multiple sources
* Evidence-based summarization
* Source attribution
* Handling conflicting information

### LLM Integration

The project also explores:

* OpenAI API integration
* Prompt construction
* Context injection
* Passing external information to an LLM
* Source-grounded generation
* Citation-aware responses
* Basic hallucination control

---

## 🛠️ Tech Stack

| Technology      | Purpose                              |
| --------------- | ------------------------------------ |
| Python          | Main programming language            |
| Tavily          | Web search and information retrieval |
| OpenAI API      | LLM-powered research synthesis       |
| `requests`      | HTTP requests                        |
| `python-dotenv` | Environment variable management      |
| Git/GitHub      | Version control                      |

---

## 📁 Project Structure

```text
Personal-AI-Research-Assistant/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── main.py
├── search.py
└── llm.py
```

### `main.py`

The main application entry point.

Responsible for:

* accepting the user's question
* triggering the search
* passing results to the LLM
* displaying the final research result

#
