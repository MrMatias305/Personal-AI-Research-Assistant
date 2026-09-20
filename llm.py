import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam
from pydantic import BaseModel

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


class Source(BaseModel):
    id: int
    title: str
    url: str

class ResearchResult(BaseModel):
    summary: str
    key_points: list[str]
    sources: list[Source]


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

    response = client.responses.parse(
        model='gpt-5.5',
        input=[
            EasyInputMessageParam(
                role="system",
                content="""
        You are a personal AI research assistant.

        Use only the provided sources to answer the user's question.

        Rules:
        - Synthesize information across the sources.
        - Do not invent unsupported facts.
        - Identify important key points.
        - Cite claims using source numbers such as [1], [2].
        - If sources disagree, mention the disagreement.
        - Only include sources that were actually provided.
        """
            ),
            EasyInputMessageParam(
                role="user",
                content=f"""
        Research question:

        {question}

        Retrieved sources:

        {research_context}
        """
            )
        ],
        text_format=ResearchResult
    )

    return response.output_parsed