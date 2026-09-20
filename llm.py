import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def build_research_context(results):
    context = []

    for i, result in enumerate(results, start=1):
        context.append(
            f"""
            SOURCE {i}
            TITLE {result['title']}
            URL {result['url']}
            CONTENT {result['content']}
"""
        )
    return "\n".join(context)


def summarize_research(question, results):
    research_context = build_research_context(results)

    prompt = f"""
    You are a personal AI research assistant.

    The user asked:
    
    {question}
    
    Below are web sources retrieved for this question:
    
    {research_context}
    
    Using ONLY the information provided in the sources:
    
    1. Write a clear summary answering the user's question.
    2. Identify the most important key points.
    3. Cite the relevant source numbers like [1], [2], etc.
    4. Do not invent information that is not supported by the sources.
    5. If the sources disagree or information is uncertain, mention that.
    
    Return your answer as JSON with exactly this structure:

    {{
        "summary": "A concise research summary.",
        "key_points": [
            "Important point 1",
            "Important point 2",
            "Important point 3"
        ],
        "sources": [
            {{
                "id": 1,
                "title": "Source title",
                "url": "Source URL"
            }}
        ]
    }}
    """

    response = client.responses.create(
        model='gpt-5.5',
        input=prompt
    )

    return response.output_text