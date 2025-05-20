import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("OPENROUTER_API_KEY not set in .env")

# Configure OpenAI client for OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def analyze_drug_interaction(drugs):
    drug_list = "\n".join(f"- {drug}" for drug in drugs)

    prompt = (
        f"You are a licensed clinical pharmacist. Analyze the drug interactions for the following medications:\n"
        f"{drug_list}\n\n"
        "Respond using this exact markdown format:\n"
        "### 1. Risks and Side Effects\n"
        "(List potential risks and side effects as bullet points)\n\n"
        "### 2. Drug Interactions\n"
        "(Explain how these drugs might interact with one another)\n\n"
        "### 3. Conclusion and Recommendation\n"
        "(Summarize whether this combination is safe and what precautions or advice should be considered)\n\n"
        "Use professional and concise language suitable for healthcare professionals."
    )

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
