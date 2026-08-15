# System Lessons Learned & Error Ledger

## Purpose
This ledger records historical pitfalls, technical snags, and architectural solutions discovered during development. Any future session or CLI instance must review this file to prevent repeating past mistakes.

---

## Log Entries

### 1. Terminal Quoting & Inline Python Scripts
- **Date:** 2026-08-15
- **Pitfall:** Running complex multi-line Python scripts via inline `python3 -c '...'` commands causes syntax errors due to shell quote expansion and escaped backslashes.
- **Root Cause:** Bash interprets nested quotes and backticks before passing them to Python.
- **Guardrail:** Never write multi-line Python scripts inline in the terminal. Always write them to a `.py` file using `cat << 'EOF'` and execute the file directly.

### 2. Raw JSON Output Mix-ups in Chat
- **Date:** 2026-08-15
- **Pitfall:** Pasting raw JSON text blocks directly into chat without code fences causes the terminal to attempt execution, resulting in command-not-found errors.
- **Root Cause:** Terminal treats unformatted text lines as shell commands when pasted.
- **Guardrail:** Always enclose scripts, configs, and file data in properly formatted code blocks.
