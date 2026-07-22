import ollama

MODEL_NAME = "llama3"


def check_drug_interactions(drugs: list[str]):

    if len(drugs) < 2:
        return "Please provide at least two medicines."

    medicine_list = "\n".join(f"- {drug}" for drug in drugs)

    prompt = f"""
You are an experienced clinical pharmacology AI assistant.

Analyze the following medicines for possible drug-drug interactions.

Medicines:
{medicine_list}

Return your answer in exactly this format:

## Drug Interaction Summary

### Interactions
- ...

### Severity
(Low / Moderate / High)

### Possible Side Effects
- ...

### Recommendation
- ...

If there are no significant interactions, clearly say so.

Do not invent medicines that are not listed.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]