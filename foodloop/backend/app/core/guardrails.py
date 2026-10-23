import re
from typing import Tuple


PHONE_REGEX = re.compile(r"(\+?91[\-\s]?)?[6789]\d{9}|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b")
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# Known adversarial jailbreak and prompt-override keywords
SUSPICIOUS_PATTERNS = [
    r"ignore.*(instruction|rule|guideline|policy)",
    r"system prompt",
    r"system override",
    r"override",
    r"you are now",
    r"mark.*safe",
    r"bypass.*safety",
    r"bypass",
    r"approve.*food",
    r"disregard",
    r"jailbreak",
]


def redact_pii(text: str) -> Tuple[str, bool]:
    """
    Redacts phone numbers and emails from untrusted text before LLM inference.
    Returns (cleaned_text, had_pii).
    """
    if not text:
        return "", False
        
    cleaned = text
    had_pii = False
    
    if PHONE_REGEX.search(cleaned):
        cleaned = PHONE_REGEX.sub("[PHONE_REDACTED]", cleaned)
        had_pii = True
        
    if EMAIL_REGEX.search(cleaned):
        cleaned = EMAIL_REGEX.sub("[EMAIL_REDACTED]", cleaned)
        had_pii = True
        
    return cleaned, had_pii


def sanitize_untrusted_input(text: str) -> Tuple[str, bool]:
    """
    Sanitizes user input and flags suspected prompt injections.
    Wraps content into secure isolation boundaries.
    """
    if not text:
        return "", False
        
    is_suspicious = False
    lower_text = text.lower()
    
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, lower_text):
            is_suspicious = True
            break
            
    # Redact PII first
    sanitized, _ = redact_pii(text)
    
    # Isolate within strict XML/Delimited boundary
    isolated = f"<UNTRUSTED_USER_CONTENT>\n{sanitized.strip()}\n</UNTRUSTED_USER_CONTENT>"
    return isolated, is_suspicious
