from App.ai.summarizer import summarize_report

report = """
Hemoglobin: 13.5 g/dL
WBC: 7600 /uL
Platelets: 250000 /uL
Blood Sugar: 95 mg/dL
"""

summary = summarize_report(report)

print("\n===== AI SUMMARY =====\n")
print(summary)