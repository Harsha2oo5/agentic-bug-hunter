import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"

def validate_issue(code_context, finding):

    prompt = f"""
You are an expert in RDI C++ API validation.

Suspicious Line:
{finding["line_text"]}

Full Code:
{code_context}

Explain the issue and provide a corrected full version of the code.

Respond strictly in JSON:

{{
 "valid_bug": true/false,
 "explanation": "...",
 "corrected_code": "...",
 "confidence": 0.0
}}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "")