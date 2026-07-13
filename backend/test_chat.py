from App.ai.chatbot import ask_doctor

question = "Summarize the uploaded report."

answer = ask_doctor(question)

print("\n===== AI ANSWER =====\n")

print(answer)