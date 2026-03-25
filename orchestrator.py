import json
import re
from static_engine import analyze_code
from validator_agent import validate_issue

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None
    return None


def process_code(code):
    findings = analyze_code(code)

    if not findings:
        # Still pass through LLM for semantic validation
        findings = [{
            "line_number": None,
            "line_text": "General semantic review",
            "rule_tag": "semantic_review",
            "static_confidence": 0.5
        }]

    best_result = None
    best_confidence = 0

    for finding in findings:
        validation_raw = validate_issue(code, finding)
        validation = extract_json(validation_raw)

        if not validation:
            continue

        combined_confidence = (
            0.6 * float(validation.get("confidence", 0)) +
            0.4 * finding["static_confidence"]
        )

        if combined_confidence > best_confidence:
            best_confidence = combined_confidence
            best_result = validation

    if not best_result:
        return {
            "explanation": "Unable to validate code.",
            "corrected_code": code
        }

    return {
        "explanation": best_result.get("explanation", ""),
        "corrected_code": best_result.get("corrected_code", code)
    }