from App.services.guideline_search import search_guidelines

print("Starting search...")

try:
    results = search_guidelines("What is hypertension?")

    print(f"Found {len(results)} results")

    for i, result in enumerate(results, 1):
        print("=" * 60)
        print(f"Result {i}")
        print(result[:300])

except Exception as e:
    import traceback
    traceback.print_exc()