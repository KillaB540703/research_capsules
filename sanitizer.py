import re

FLUFF_PATTERNS = [
    r"it is important to note that",
    r"delve into",
    r"testament to",
    r"plays a crucial role",
    r"in conclusion",
    r"as an ai",
    r"it's fascinating to see",
    r"overall, the landscape",
]

def sanitize_payload(text_content):
    """
    Strips AI fluff and checks for mandatory numerical/factual density.
    Returns (cleaned_text, is_flagged)
    """
    cleaned = text_content
    flagged = False
    
    for pattern in FLUFF_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            flagged = True
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    has_metrics = bool(re.search(r'\d+(\.\d+)?(%|inches|ft|gpm|percent|status|advisory)', cleaned, re.IGNORECASE))
    
    if not has_metrics and len(cleaned.strip()) > 50:
        flagged = True

    return cleaned.strip(), flagged
