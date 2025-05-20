import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set in .env")
client = OpenAI(api_key=api_key)

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
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
