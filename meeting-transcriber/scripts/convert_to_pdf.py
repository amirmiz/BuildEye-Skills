"""
Convert Hebrew Markdown files to RTL PDF using Chrome headless.
Usage: python convert_to_pdf.py <file1.md> [file2.md ...]

Outputs <file>.pdf alongside each input file.
Requires: Chrome at C:\Program Files\Google\Chrome\Application\chrome.exe
          pip install markdown
"""
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import markdown

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@page { size: A4; margin: 18mm 20mm 18mm 20mm; }
* { box-sizing: border-box; }
body {
    font-family: Arial, 'Segoe UI', sans-serif;
    direction: rtl; unicode-bidi: embed;
    font-size: 11pt; line-height: 1.75;
    color: #1a1a1a; background: white;
}
h1 {
    font-size: 18pt; font-weight: bold; color: #1a3c5e;
    border-bottom: 2.5px solid #1a3c5e; padding-bottom: 5px;
    margin: 0 0 12px 0; text-align: right; page-break-after: avoid;
}
h2 {
    font-size: 13pt; font-weight: bold; color: #1a3c5e;
    border-bottom: 1px solid #94b8d4; padding-bottom: 3px;
    margin: 20px 0 6px 0; text-align: right; page-break-after: avoid;
}
h3 {
    font-size: 11.5pt; font-weight: bold; color: #2e5f8a;
    margin: 14px 0 4px 0; text-align: right; page-break-after: avoid;
}
h4 { font-size: 11pt; font-weight: bold; margin: 10px 0 4px 0; text-align: right; }
p { margin: 2px 0 8px 0; text-align: right; }
ul, ol { margin: 2px 0 8px 0; padding-right: 22px; padding-left: 0; text-align: right; }
li { margin-bottom: 4px; text-align: right; }
li > ul, li > ol { margin-top: 2px; margin-bottom: 2px; }
strong, b { font-weight: bold; }
em, i { font-style: italic; }
blockquote {
    border-right: 4px solid #1a3c5e; border-left: none;
    margin: 8px 0 10px 30px; padding: 7px 14px 7px 7px;
    background: #eef5fb; color: #2a2a2a; font-style: italic;
    border-radius: 0 4px 4px 0;
}
blockquote p { margin: 0; }
code {
    font-family: Consolas, monospace; background: #f0f0f0;
    padding: 1px 5px; border-radius: 3px; font-size: 9.5pt;
    direction: ltr; unicode-bidi: isolate; display: inline-block;
}
table {
    width: 100%; border-collapse: collapse;
    margin: 10px 0 14px 0; font-size: 10pt;
    direction: rtl; page-break-inside: avoid;
}
th {
    background-color: #1a3c5e; color: white;
    padding: 7px 11px; text-align: right; font-weight: bold;
    border: 1px solid #15324f;
}
td { padding: 6px 11px; text-align: right; border: 1px solid #c4d8ea; vertical-align: top; }
tr:nth-child(even) td { background-color: #f0f6fb; }
tr:nth-child(odd) td  { background-color: #ffffff; }
hr { border: none; border-top: 1.5px solid #adc6d8; margin: 14px 0; }
a { color: #1a5fa8; text-decoration: none; }
"""


def md_to_html(md_text: str, title: str) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>{body}</body>
</html>"""


def convert_file(md_path: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    html = md_to_html(text, md_path.stem)

    tmp_dir = Path(tempfile.mkdtemp())
    html_path = tmp_dir / "doc.html"
    html_path.write_text(html, encoding="utf-8")

    pdf_path = md_path.with_suffix(".pdf")
    try:
        result = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--disable-dev-shm-usage",
             f"--print-to-pdf={pdf_path}", "--print-to-pdf-no-header",
             str(html_path)],
            capture_output=True, timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    size_kb = pdf_path.stat().st_size // 1024
    print(f"Successfully created: {pdf_path.name}  ({size_kb} KB)")
    return pdf_path


def main(files):
    if not files:
        print("Usage: python convert_to_pdf.py <file1.md> [file2.md ...]")
        sys.exit(1)

    ok, fail = 0, 0
    for f in files:
        p = Path(f)
        if not p.exists():
            print(f"  MISSING: {f}")
            fail += 1
            continue
        try:
            convert_file(p)
            ok += 1
        except Exception as e:
            print(f"  ERROR: {p.name} — {e}")
            fail += 1

    print(f"\nDone: {ok} OK, {fail} failed.")


if __name__ == "__main__":
    main(sys.argv[1:])
