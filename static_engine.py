import re

def extract_rdi_methods(code):
    pattern = r'\.\s*(\w+)\s*\('
    return re.findall(pattern, code)


def detect_unknown_methods(code):
    findings = []
    lines = code.split("\n")

    # Common RDI method patterns
    known_prefixes = [
        "get", "set", "read", "write",
        "pin", "label", "burst", "execute",
        "vForce", "iForce", "vMeas", "iMeas",
        "samples", "begin", "end", "wait"
    ]

    for i, line in enumerate(lines):
        matches = re.findall(r'\.\s*(\w+)\s*\(', line)

        for method in matches:
            if not any(method.startswith(prefix) for prefix in known_prefixes):
                findings.append({
                    "line_number": i + 1,
                    "line_text": line.strip(),
                    "rule_tag": "suspicious_method_name",
                    "static_confidence": 0.8
                })

    return findings


def detect_unmatched_rdi_blocks(code):
    findings = []
    begin_count = code.count("RDI_BEGIN")
    end_count = code.count("RDI_END")

    if begin_count != end_count:
        findings.append({
            "line_number": None,
            "line_text": "RDI_BEGIN / RDI_END mismatch",
            "rule_tag": "rdi_block_mismatch",
            "static_confidence": 0.9
        })

    return findings


def detect_incomplete_chaining(code):
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if "rdi." in line and not line.strip().endswith((";", "}", "{")):
            findings.append({
                "line_number": i + 1,
                "line_text": line.strip(),
                "rule_tag": "incomplete_chain",
                "static_confidence": 0.7
            })

    return findings


def analyze_code(code):
    findings = []
    findings.extend(detect_unknown_methods(code))
    findings.extend(detect_unmatched_rdi_blocks(code))
    findings.extend(detect_incomplete_chaining(code))
    return findings