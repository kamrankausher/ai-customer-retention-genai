import ollama
import json


def generate_retention_bundle(customer_profile: dict) -> dict:
    """
    Generates structured retention intelligence using a local LLM.
    Returns a dictionary with explanation, decision, and customer message.
    """

    prompt = f"""
You are a senior customer retention strategist working for a telecom company.

You are given a customer profile in JSON format.

Your task:
1. Explain WHY the customer may churn
2. Decide WHAT retention action should be taken
3. Write a PROFESSIONAL customer-facing message

STRICT RULES:
- Respond ONLY in valid JSON
- Do NOT add extra text
- Do NOT explain outside JSON
- Do NOT use placeholders like YOUR NAME or COMPANY NAME
- ALWAYS sign the message as: Customer Success Team
- Keep tone warm, concise, and business-ready

JSON FORMAT:
{{
  "risk_explanation": "string",
  "retention_decision": "string",
  "customer_message": "string"
}}

Customer Profile:
{json.dumps(customer_profile, indent=2)}
"""

    # ---------- Call LLM safely ----------
    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        raw_output = response["message"]["content"]

    except Exception:
        return {
            "risk_explanation": "AI system temporarily unavailable.",
            "retention_decision": "No decision available.",
            "customer_message": "Thank you for your patience."
        }

    # ---------- Parse JSON safely ----------
    try:
        structured_output = json.loads(raw_output)

    except json.JSONDecodeError:
        structured_output = {
            "risk_explanation": "Unable to generate explanation at this time.",
            "retention_decision": "No action recommended.",
            "customer_message": "Thank you for being a valued customer."
        }

    return structured_output
