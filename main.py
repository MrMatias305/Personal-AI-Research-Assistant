from llm import summarize_research
from search import web_search


def main():
    question = input("\nWhat do you want to research?\n> ")

    print("\nSearching for relevant sources...")

    results = web_search(question)

    print(f"\nFound {len(results)} sources.")

    print("\nAnalyzing sources with AI...")

    answer = summarize_research(question, results)

    print("\n" + "=" * 60)
    print("RESEARCH RESULT")
    print("=" * 60)

    print(answer)


if __name__ == "__main__":
    main()
