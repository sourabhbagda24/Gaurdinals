# 🛡️ Guardinals — PII Masking Pipeline

**Guardinals** is a lightweight Python pipeline that automatically detects and redacts Personally Identifiable Information (PII) from raw transaction messages and text datasets — purpose-built for Indian financial data.

---

## ✨ Features

- 🔍 Detects **10+ PII types** using regex patterns
- 🇮🇳 Tailored for **Indian data** — Aadhaar, PAN, IFSC, PIN codes
- 🏦 Covers **financial identifiers** — bank account numbers, card numbers
- 📧 Handles **contact info** — emails, phone numbers, URLs, addresses
- ⚡ Fast, single-file pipeline — no external NLP models required
- 📁 Processes bulk `.csv` / `.txt` datasets and outputs a clean masked file

---

## 🔐 Supported PII Types

| Tag | What It Masks |
|-----|--------------|
| `[PHONE_REDACTED]` | Mobile and landline numbers (with country codes) |
| `[EMAIL_REDACTED]` | Email addresses |
| `[ACCOUNT_REDACTED]` | Bank / account numbers (9–18 digits) |
| `[CARD_REDACTED]` | Credit / debit card numbers (13–16 digits) |
| `[AADHAAR_REDACTED]` | Indian Aadhaar numbers (`XXXX XXXX XXXX`) |
| `[PAN_REDACTED]` | Indian PAN numbers (`ABCDE1234F`) |
| `[IFSC_REDACTED]` | Bank IFSC codes (`SBIN0001234`) |
| `[PINCODE_REDACTED]` | Indian 6-digit postal PIN codes |
| `[URL_REDACTED]` | HTTP/HTTPS URLs and www links |
| `[ADDRESS_REDACTED]` | Street addresses with keywords like road, sector, nagar |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- No external dependencies — uses only the Python standard library

### Installation

```bash
git clone https://github.com/your-username/guardinals.git
cd guardinals
```

### Configuration

Edit the two paths at the top of `guardinals.py`:

```python
INPUT_PATH    = r"path/to/your/transactions_dataset.csv"
OUTPUT_FOLDER = r"path/to/your/output/folder"
```

### Run

```bash
python guardinals.py
```

The masked output is saved as `masked_messages.txt` inside your specified output folder.

---

## 📂 Project Structure

```
guardinals/
├── guardinals.py        # Main pipeline script
└── README.md
```

---

## 🧪 Example

**Input:**
```
Hello, please transfer ₹5000 to account 987654321012 from card 4111 1111 1111 1111.
Contact me at rajesh.kumar@gmail.com or +91-98765-43210. My Aadhaar is 1234 5678 9012.
```

**Output:**
```
Hello, please transfer ₹5000 to account [ACCOUNT_REDACTED] from card [CARD_REDACTED].
Contact me at [EMAIL_REDACTED] or [PHONE_REDACTED]. My Aadhaar is [AADHAAR_REDACTED].
```

---

## ⚙️ How It Works

1. **Load** — reads every line from the input file
2. **Match & Mask** — applies regex patterns in a safe priority order (specific patterns first, generic ones last) to avoid partial overlaps
3. **Export** — writes the masked lines to `masked_messages.txt`
4. **Report** — prints a summary of total messages processed and how many contained PII

Pattern priority order ensures correctness:
```
EMAIL → URL → CARD → AADHAAR → PAN → IFSC → ACCOUNT → PHONE → ADDRESS → PIN_CODE
```

---

## 📊 Output Summary

After each run, Guardinals prints:

```
============================================================
 PIPELINE COMPLETE!
 Total messages     : 1500
 Messages redacted  : 1342
 Output saved at    : D:\NLP\Guardinals\CLEANED MESSAGE\masked_messages.txt
============================================================
```

---

## ⚠️ Limitations

- Regex-based — may have false positives on numeric strings that resemble account numbers or PIN codes
- Does not handle **named entity recognition** (names, organizations) — consider integrating spaCy or a transformer model for that
- Designed for **Indian PII formats**; international formats (SSN, NIN, etc.) are not covered out of the box

---

## 🤝 Contributing

Pull requests are welcome! To add a new PII pattern:

1. Add your regex to the `PATTERNS` dict
2. Add a redaction tag to `MASK_TAG`
3. Insert the key at the appropriate position in `ORDER`

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> Built with ❤️ for privacy-first data pipelines.
