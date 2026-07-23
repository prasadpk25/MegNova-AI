from App.services.guideline_chat import ask_guideline

question = input("Ask: ")

answer = ask_guideline(question)

print("\n")
print("=" * 80)
print(answer)