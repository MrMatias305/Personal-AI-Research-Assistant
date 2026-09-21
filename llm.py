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
    content: str

class Claim(BaseModel):
    text: str
    source_ids: list[int]
    evidence: list[str]

class ResearchResult(BaseModel):
    summary: str
    claims: list[Claim]
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
        
        - Synthesize information across the provided sources.
        - Do not invent unsupported facts.
        - Every claim must be supported by evidence from the provided sources.
        - For every claim, provide the IDs of the sources that support it.
        - For every claim, provide the specific evidence from those sources.
        - Do not cite a source unless it actually supports the claim.
        - If multiple sources support a claim, include all relevant source IDs.
        - If sources disagree, represent the disagreement accurately.
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
        
        Create a research result based only on these sources.
        
        For each important claim:
        1. State the claim.
        2. Identify the source IDs supporting the claim.
        3. Provide the relevant evidence from those sources.
        """
            )
        ],
        text_format=ResearchResult
    )

    return response.output_parsed