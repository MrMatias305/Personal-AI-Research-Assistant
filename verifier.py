import os

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses import EasyInputMessageParam
from pydantic import BaseModel


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class VerificationResult(BaseModel):
    claim: str
    supported: bool
    explanation: str


# Verify claim
def verify_claim(claim, source):

    response = client.responses.parse(
        model='gpt-5.5',
        input=[
            EasyInputMessageParam(
                role='system',
                content="""
    You are a research evidence verifier.
    
    Your task is to determine whether the provided source
    actually supports the provided claim.
    
    Rules:
    - Use only the provided source.
    - Do not use outside knowledge.
    - Mark supported as true only when the source provides
      sufficient evidence for the claim.
    - If the source only partially supports the claim,
      mark supported as false.
    - Explain your reasoning briefly.
                """
            ),
            EasyInputMessageParam(
                role='user',
                content=f"""
    CLAIM:
    
    {claim.text}
    
    SOURCE:
    
    Title: {source.title}
    
    URL: {source.url}
    
    Content:
    
    {source.content}
                """
            )
        ],
        text_format=VerificationResult,
    )

    return response.output_parsed