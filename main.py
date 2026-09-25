from grounding import validate_claims
from llm import summarize_research
from search import web_search


def main():
    question = input("\nWhat do you want to research?\n> ")

    print("\nSearching for relevant sources...")

    results = web_search(question)

    print(f"\nFound {len(results)} sources.")

    print("\nAnalyzing sources with AI...")

    research = summarize_research(question, results)
    validation_results = validate_claims(research)

    # Check validation
    print("\nGROUNDING CHECK")
    print("-" * 60)

    for result in validation_results:
        status = "VALID" if result["valid"] else "INVALID"
        print(f"{result['claim']}: {status}")

    print("="*60)
    print("RESEARCH RESULTS")
    print("="*60)

    print("\nSUMMARY")
    print("-" * 60)
    print(research.summary)

    print("\nClaims")
    print("-" * 60)
    for claim in research.claims:
        print(f"- {claim.text}")

        print(f"    Sources: {claim.source_ids}")

        print(f"    Evidence:")
        for evidence in claim.evidence:
            print(f"    - {evidence}")

    print("\nSOURCES")
    print("-" * 60)
    for source in research.sources:
        print(f"[{source.id}] {source.title}")
        print(f"   {source.url}")


if __name__ == "__main__":
    main()
