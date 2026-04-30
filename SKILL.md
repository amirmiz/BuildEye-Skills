---
name: meeting-transcriber
description: >
  BuildEye meeting transcription and summarization pipeline. Use this skill whenever the user
  wants to transcribe, summarize, or process audio recordings of customer discovery or research
  meetings — especially in Hebrew. Triggers on phrases like "תמלל פגישה", "תמלל את ההקלטה",
  "סכם פגישה", "צור סיכום", "המר ל-PDF", "עבד הקלטה", or any combination of transcription +
  summary + PDF for meeting recordings. Also triggers when the user mentions .m4a/.mp3 files
  in the context of meetings or interviews. The pipeline covers: discovering audio files,
  transcribing with faster-whisper large-v3 (Hebrew), writing a detailed 2-3 page Hebrew
  summary, writing a 1-page executive summary, and converting all outputs to RTL Hebrew PDFs.
  Always use this skill for any BuildEye meeting recording workflow, even if the user only asks
  for one step (e.g., "just convert to PDF" or "just summarize").
---

# Meeting Transcriber — BuildEye Pipeline

You are running a 5-phase pipeline for BuildEye customer discovery recordings. BuildEye is an
Israeli laser-scanning/BIM company doing interviews with FM managers and asset managers about
their CMMS systems (Visit, MyTower, etc.). All communication with the user is in **Hebrew**.

The pipeline is designed to be resumable — detect which phases are already done and skip them.

---

## Phase 0 — Detect State & Ask the User (in Hebrew)

Start by scanning the recordings folder for audio files and existing outputs:

**Default recordings folder:**
```
C:\Users\1\BuildEye\MGMT - Documents\פיתוח\BIMFM\הקלטות פגישות\
```

List all audio files (`.m4a`, `.mp3`, `.wav`, `.ogg`) found in that folder.
For each file, check whether `.txt`, `- סיכום פגישה.md`, `- סיכום חד-עמודי.md`, and `.pdf` already exist.

Then greet the user **in Hebrew** and show the status table. Example:

```
שלום! מצאתי את ההקלטות הבאות בתיקייה:

| קובץ | תמלול | סיכום מפורט | סיכום חד-עמודי | PDF |
|------|--------|-------------|----------------|-----|
| Gur Gal CBRE.m4a | ✓ | ✓ | ✓ | ✓ |
| New Recording.m4a | ✗ | ✗ | ✗ | ✗ |

אילו קבצים תרצה לעבד? (תוכל לציין שמות או לכתוב "הכל")
```

Wait for the user's answer before proceeding. If the user specifies only some phases
(e.g., "just create PDFs"), skip to the relevant phase.

---

## Phase 1 — Transcription

For each selected audio file that **does not yet have a .txt**, run transcription.

Transcription takes **30–60 minutes per file on CPU**. Tell the user upfront and run as a
background task so the conversation stays responsive.

Use the bundled script `scripts/transcribe_one.py`:

```bash
cd "<recordings_folder>"
python -X utf8 "<skill_dir>/scripts/transcribe_one.py" "<audio_file>"
```

The script outputs `<filename>.txt` and `<filename>.srt` in the same folder as the audio.

**Monitor progress:** tail the output every few minutes and report segment progress to the user.
When done, confirm: "התמלול של [שם קובץ] הושלם — [N] סגמנטים, [X] דקות."

---

## Phase 2 — Detailed Summary (סיכום פגישה)

For each recording that has a `.txt` but **no `- סיכום פגישה.md`**, write the detailed report.

### How to read the transcript

The `.txt` file is a plain Hebrew transcript (no speaker labels — Whisper doesn't diarize).
Read it in chunks (the file may be 100–200KB). The `.srt` file has the same content with
timestamps — use it to look up timestamps for key quotes.

### Speaker attribution approach

BuildEye team (questioners) vs. interviewee (answers) — infer from context:
- Lines describing a CMMS system's behavior, daily workflows, complaints = **interviewee**
- Lines asking probing questions, presenting BuildEye's vision = **BuildEye team**
- Mark uncertain attributions as "(שיוך לא ודאי)"

### Output: `{base_name} - סיכום פגישה.md`

Write in Hebrew. Target 2–3 pages. Use this structure (adapt section titles to what's relevant):

```markdown
# סיכום פגישה — [שם המרואיין], [ארגון], [נכס/תפקיד]

**תאריך:** [היום]  **אורך:** ~[N] דקות  **מערכת מרכזית:** [Visit/MyTower/אחר]

**משתתפים (לפי הסקה):**
- [ארגון]: [שם] ([תפקיד])
- BuildEye: אמיר + המציג

**מטרת הפגישה:** [1-2 משפטים]

> הערה: התעתיק נוצר אוטומטית ללא תיוג דוברים. שיוך מבוסס על הקשר.

---

## 1. הקשר ארגוני ותפעולי
[ארגון, נכס, גודל, מערכות משולבות — כולל טבלת מערכות אם רלוונטי]

## 2. יתרונות המערכת הנוכחית
[מה עובד טוב — רשימה ממוספרת]

## 3. חסרונות ונקודות כאב
[כאבים תפעוליים, כאבי אנליטיקס, כאבי ארכיטקטורה — תתי-סעיפים]

## 4. תובנות על תהליכי עבודה
[אונבורדינג, ניהול ידע, ספקים, מדדים]

## 5. העדפות טכנולוגיות
[מובייל/דסקטופ, AI, WhatsApp, BIM, 2D vs 3D]

## 6. הזדמנויות עבור BuildEye
> *סעיף זה הוא פרשנות של BuildEye, לא דברי המרואיין.*

| פער שזוהה | מה נאמר | הזדמנות |
|---|---|---|

## 7. ציטוטים נבחרים עם חותמות זמן
[6-10 ציטוטים מרכזיים עם timestamp מה-.srt]
```

---

## Phase 3 — Executive Summary (סיכום חד-עמודי)

For each recording that has a `- סיכום פגישה.md` but **no `- סיכום חד-עמודי.md`**, write
the 1-page summary.

### Output: `{base_name} - סיכום חד-עמודי.md`

Rules: bullets only, no quotes, Hebrew, fits on one printed page (~400 words max).

```markdown
# סיכום חד-עמודי — [שם], [ארגון]

**תאריך:** | **אורך:** | **מערכת:** [Visit/MyTower/...]

---

## מי הם המשתתפים
- [שם]: [תפקיד + 1 משפט רקע]

## על המערכת
- [3-5 bullets על הפלטפורמה]

## מה עובד טוב
- [3-5 bullets]

## פערים ובעיות
- [4-6 bullets — הכי חשובים]

## תובנות מרכזיות
- [3-5 bullets — insights שלא נכנסו לקטגוריות אחרות]

## המלצות / השלכות לBuilEye
- [2-4 bullets]
```

---

## Phase 4 — PDF Conversion

For each `.md` file (both `- סיכום פגישה.md` and `- סיכום חד-עמודי.md`) that has **no
corresponding `.pdf`**, convert to PDF.

Use the bundled script `scripts/convert_to_pdf.py`:

```bash
cd "<recordings_folder>"
python -X utf8 "<skill_dir>/scripts/convert_to_pdf.py" "<md_file_1>" "<md_file_2>" ...
```

The script uses Chrome headless for perfect Hebrew RTL rendering and saves `<filename>.pdf`
alongside each `.md` file.

---

## Completion

When all phases are done, summarize in Hebrew:

```
הושלם! הנה מה שנוצר:

תמלולים: [N קבצים]
סיכומים מפורטים: [N קבצים]
סיכומים חד-עמודיים: [N קבצים]
קובצי PDF: [N קבצים]

כל הקבצים נשמרו ב:
C:\Users\1\BuildEye\MGMT - Documents\פיתוח\BIMFM\הקלטות פגישות\
```

---

## Key Context for Summaries

Keep this in mind when writing all summaries:

- **BuildEye's goal**: understand how FM/asset managers use their current CMMS, find pain
  points, and identify product opportunities for a new BIM-connected FM platform.
- **The interviewees** are typically Israeli FM professionals, often technical, using Hebrew
  with English code-switching for product names (Visit, MyTower, KPIs, SLA, API, CAPEX/OPEX).
- **The most valuable insights** are concrete: workflows that break down, metrics nobody
  measures, integrations that don't exist, things still done on paper or in Excel/WhatsApp.
- **Opportunities section** = BuildEye's analysis, not the interviewee's words. Mark clearly.
- See `references/summary-examples.md` for real examples from completed summaries.
