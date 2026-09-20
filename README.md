# Personal AI Research Assistant

A personal AI research assistant that takes a research question, searches the web for relevant sources, and uses an LLM to synthesize the retrieved information into a structured research result.

The project is being built incrementally to understand the fundamentals of **AI research workflows, information retrieval, LLM integration, structured outputs, and eventually citation grounding**.

---

## Current Version

**V1.3 — Native Structured LLM Output**

Current pipeline:

```text
Research Question
       ↓
Tavily Web Search
       ↓
Retrieved Sources
       ↓
Research Context
       ↓
OpenAI Responses API
       ↓
Pydantic Structured Output
       ↓
Research Result
```

---

## Features

The current version can:

* Accept a research question from the terminal
* Search the web using Tavily
* Retrieve multiple relevant sources
* Extract source titles, URLs, and content
* Build a research context from the retrieved sources
* Send the research question and source context to an OpenAI model
* Ask the LLM to synthesize information only from the provided sources
* Produce structured research output
* Return:

  * Summary
  * Key points
  * Sources
* Validate the LLM output using a Pydantic schema
* Use OpenAI's `responses.parse()` for native structured output

---

## What I'm Learning

This project is mainly a hands-on learning project.

### 1. Information Retrieval

The LLM should not be the only source of information.

Instead:

```text
Question
   ↓
Retrieve external information
   ↓
Give evidence to the LLM
   ↓
Generate a research result
```

This introduces the basic idea behind retrieval-augmented AI systems.

---

### 2. LLM Integration

The project uses the OpenAI Python SDK to send the research question and retrieved source material to an LLM.

The application separates:

* Retrieval
* Context preparation
* LLM processing
* Output handling

---

### 3. Structured LLM Output

Instead of asking the model to return arbitrary text or manually formatted JSON, the project now uses a Pydantic schema.

Example:

```python
class ResearchResult(BaseModel):
    summary: str
    key_points: list[str]
    sources: list[Source]
```

The application can therefore work with:

```python
research.summary
research.key_points
research.sources
```

rather than manually parsing a large text response.

---

### 4. Native Parsing with `responses.parse()`

The OpenAI Responses API is used with:

```python
client.responses.parse(...)
```

and a Pydantic model is provided through:

```python
text_format=ResearchResult
```

The parsed result is then available through:

```python
response.output_parsed
```

This creates a cleaner boundary between the LLM and the Python application:

```text
LLM
 ↓
Structured response
 ↓
Pydantic object
 ↓
Python application
```

---

## Tech Stack

| Technology    | Purpose                              |
| ------------- | ------------------------------------ |
| Python        | Core application                     |
| OpenAI API    | LLM processing                       |
| Tavily API    | Web search and information retrieval |
| Pydantic      | Structured output validation         |
| python-dotenv | Environment variable management      |
| Requests      | HTTP requests to Tavily              |
| Git / GitHub  | Version control                      |

---

## Project Structure

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

Responsible for orchestrating the application.

```text
User Input
    ↓
Search
    ↓
LLM Research
    ↓
Display Result
```

### `search.py`

Responsible for web retrieval.

It:

1. Sends the research question to Tavily
2. Retrieves search results
3. Extracts:

   * Title
   * URL
   * Content
4. Returns the results as Python data

### `llm.py`

Responsible for:

* Building the research context
* Defining the Pydantic output schema
* Sending the research request to OpenAI
* Parsing the structured response

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit `.env` to Git.

The `.gitignore` contains:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Personal-AI-Research-Assistant
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure the project has:

```text
openai
python-dotenv
requests
pydantic
```

---

## Running the Application

Start the application with:

```bash
python main.py
```

The application asks:

```text
What do you want to research?
>
```

For example:

```text
What is artificial intelligence?
```

The application then:

```text
Searching for relevant sources...

Found 5 sources.

Analyzing sources with AI...
```

and produces a structured research result.

---

## Example Output

```text
============================================================
RESEARCH RESULTS
============================================================

SUMMARY
------------------------------------------------------------
Artificial intelligence is ...

KEY POINTS
------------------------------------------------------------
- AI refers to ...
- Machine learning is ...
- AI systems can ...

SOURCES
------------------------------------------------------------
[1] Introduction to Artificial Intelligence
   https://example.com/ai

[2] What is Artificial Intelligence?
   https://example.com/artificial-intelligence
```

The exact results depend on the question and the sources retrieved by Tavily.

---

## Architecture

The current architecture deliberately keeps the application simple:

```text
                    ┌─────────────────┐
                    │  User Question  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │   search.py     │
                    │                 │
                    │  Tavily Search  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Retrieved       │
                    │ Sources         │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     llm.py      │
                    │                 │
                    │ Context + LLM   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Pydantic        │
                    │ ResearchResult  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    main.py      │
                    │                 │
                    │ Display Results │
                    └─────────────────┘
```

---

## Why Structured Output Matters

A plain LLM response might look like:

```text
Artificial intelligence is...
There are several important concepts...
Sources include...
```

A Python application would then have to figure out which part is the summary, which parts are key points, and which parts are sources.

With structured output:

```python
ResearchResult(
    summary="...",
    key_points=["...", "..."],
    sources=[
        Source(id=1, title="...", url="...")
    ]
)
```

the application already knows what each piece of information represents.

This makes the LLM output easier to:

* Validate
* Display
* Store
* Pass to other application components
* Extend into future features

---

## Current Limitations

The current system is functional, but it still has important limitations.

### Citation grounding

The LLM is instructed to cite sources using:

```text
[1]
[2]
[3]
```

However, the application does not yet independently verify that every claim is actually supported by the cited source.

For example:

```text
Claim → [2]
```

is currently generated by the LLM rather than being validated by a dedicated grounding mechanism.

This is an important area for the next version.

### Search quality

The current search implementation uses a straightforward Tavily search.

It does not yet perform:

* Query expansion
* Multiple search strategies
* Source ranking
* Duplicate removal
* Advanced relevance filtering

### Source processing

The application currently sends retrieved source content directly into the research context.

It does not yet perform sophisticated:

* Content extraction
* Chunking
* Source comparison
* Evidence extraction

---

## Development Roadmap

### Completed

* [x] Basic Python project
* [x] Tavily web search integration
* [x] Retrieve multiple sources
* [x] Build research context
* [x] OpenAI LLM integration
* [x] Structured research result
* [x] Pydantic schema
* [x] Native `responses.parse()` output
* [x] Separate retrieval and LLM responsibilities

### Next

* [ ] Improve citation grounding
* [ ] Map individual claims to supporting sources
* [ ] Improve source relevance
* [ ] Handle conflicting sources
* [ ] Improve search strategies
* [ ] Add better error handling

### Future

* [ ] Advanced web research
* [ ] Research reports
* [ ] PDF/document research
* [ ] RAG
* [ ] Persistent research history
* [ ] Vector database
* [ ] Web interface
* [ ] Research agent workflows

---

## Key Concept

The main idea behind this project is:

> **An AI research assistant should retrieve evidence first, then use an LLM to synthesize that evidence.**

Instead of:

```text
Question → LLM → Answer
```

we are building toward:

```text
Question
   ↓
Retrieve evidence
   ↓
Evaluate and organize evidence
   ↓
LLM synthesis
   ↓
Grounded research result
```

The current version implements the first major stages of this architecture.

---

## Project Status

**V1.3 — Native Structured Output**

The core research pipeline is working.

The next major challenge is moving from:

```text
LLM-generated citations
```

toward:

```text
Verified claim → Supporting evidence → Source
```

That will make the research assistant significantly more reliable.
