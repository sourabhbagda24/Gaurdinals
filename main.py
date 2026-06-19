import re
import os


# ============================================================
INPUT_PATH = r"D:\NLP\Guardinals\transactions_dataset.csv"           
OUTPUT_FOLDER = r"D:\NLP\Guardinals\CLEANED MESSAGE"    
# ============================================================

# ── Step 1: PII Patterns ───────────────────────────────────────────────────
PATTERNS = {
    "PHONE": re.compile(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3}[-.\s]?\d{3,4}\b'),
    "EMAIL": re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    "ACCOUNT": re.compile(r'\b\d{9,18}\b'),  # bank/account no.
    "CARD": re.compile(r'\b(?:\d[ -]*?){13,16}\b'),  # credit/debit card
    "AADHAAR": re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b'),  # Indian Aadhaar
    "PAN": re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'),  # Indian PAN
    "IFSC": re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b'),  # bank IFSC code
    "PIN_CODE": re.compile(r'\b\d{6}\b'),  # Indian postal pin
    "URL": re.compile(r'https?://\S+|www\.\S+'),
    "ADDRESS": re.compile(
        r'\b\d{1,5}\s+\w+(\s\w+){0,4}\s'
        r'(street|st|road|rd|avenue|ave|lane|ln|block|sector|colony|nagar|society)\b',
        re.IGNORECASE
    ),
}

MASK_TAG = {
    "PHONE": "[PHONE_REDACTED]",
    "EMAIL": "[EMAIL_REDACTED]",
    "ACCOUNT": "[ACCOUNT_REDACTED]",
    "CARD": "[CARD_REDACTED]",
    "AADHAAR": "[AADHAAR_REDACTED]",
    "PAN": "[PAN_REDACTED]",
    "IFSC": "[IFSC_REDACTED]",
    "PIN_CODE": "[PINCODE_REDACTED]",
    "URL": "[URL_REDACTED]",
    "ADDRESS": "[ADDRESS_REDACTED]",
}

# order matters — specific patterns first,after that generic .
ORDER = ["EMAIL", "URL", "CARD", "AADHAAR", "PAN", "IFSC", "ACCOUNT", "PHONE", "ADDRESS", "PIN_CODE"]


# ── Step 2: Masking Function ────────────────────────────────────────────────
def mask_sensitive(text: str) -> str:
    masked = text
    for key in ORDER:
        masked = PATTERNS[key].sub(MASK_TAG[key], masked)
    return masked


# ── Step 3: File Reader ─────────────────────────────────────────────────────
def read_messages(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


# ── Step 4: Main Pipeline ───────────────────────────────────────────────────
def run_pipeline():
    print("=" * 60)
    print(" PII MASKING PIPELINE (TXT MESSAGES)")
    print("=" * 60)

    if not os.path.isfile(INPUT_PATH):
        print(f"\n ERROR: File exist nahi karta — '{INPUT_PATH}'")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    print(f"\n Input         : {INPUT_PATH}")
    print(f" Output folder : {OUTPUT_FOLDER}\n")

    messages = read_messages(INPUT_PATH)
    print(f" Messages loaded : {len(messages)}\n")

    if not messages:
        print(" Koi message nahi mila.")
        return

    masked_lines = []
    redaction_count = 0

    for msg in messages:
        masked = mask_sensitive(msg)
        if masked != msg:
            redaction_count += 1
        masked_lines.append(masked)

    # ── Step 5: Output txt save ──────────────────────────────────────────
    output_path = os.path.join(OUTPUT_FOLDER, "masked_messages.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(masked_lines))

    print("=" * 60)
    print(" PIPELINE COMPLETE!")
    print(f" Total messages     : {len(messages)}")
    print(f" Messages redacted  : {redaction_count}")
    print(f" Output saved at    : {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()