# Campus Handbook Q&A (RAG)

Ask questions about a fictional campus handbook. Python ranks text paragraphs by keyword overlap. Gemini then generates an answer using up to two matching passages. The program shows the retrieved source files and paragraph numbers.

## Run the demo on Windows

Use Python 3.10 or newer. No extra Python packages are required.

1. Create or copy an API key from a **Free Tier** project in [Google AI Studio](https://aistudio.google.com/apikey). The default model is [Gemini 3.1 Flash-Lite](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.1-flash-lite).
2. Open this folder in File Explorer. Click the address bar, type `powershell`, and press **Enter**.
3. Run the first command and paste your key when prompted. In the same window, run the second command to start the demo.

```powershell
$env:GEMINI_API_KEY = Read-Host "Paste your Gemini API key"
py -3 rag.py "How long can I borrow books?"
```

Expect an answer mentioning **14 days**, followed by `documents/library.txt (paragraph 2)`. The key is available until you close that PowerShell window. Answer generation needs an internet connection.

On macOS or Linux, set `GEMINI_API_KEY` in your shell and use `python3` in place of `py -3`.

## Try retrieval by itself

Preview mode prints the matching passages and works without an API key.

```powershell
py -3 rag.py --preview "How long can I borrow books?"
```

Try asking `"How do I reset my campus password?"` or `"How often does the campus shuttle run?"`. To add content, place UTF-8 `.txt` files in `documents/` and separate paragraphs with blank lines. The script reads them each time it runs.

[Gemini API reference](https://ai.google.dev/api/generate-content)
