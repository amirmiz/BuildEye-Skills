# Summary Examples — Real Outputs from BuildEye Meetings

These are excerpts from the three completed summaries. Use them to calibrate tone,
depth, and structure when writing new summaries.

---

## Example: Opening / Context Section (Gur Gal CBRE)

```markdown
# סיכום פגישה — גור גל, CBRE, מגדל אלון תל אביב

**תאריך:** 28 באפריל 2026
**אורך הקלטה:** ~91 דקות
**משתתפים (לפי הסקה מההקלטה):**
- **CBRE:** גור גל (מנהל האתר), אלי (מנהל החזקה — נוכח חלקית)
- **BuildEye:** אמיר (מהנדס תוכנה), המציג (תפעול/אסטרטגיה)

## 1. הקשר ארגוני ותפעולי

- גור מנהל את **מגדל אלון תל אביב הצפוני** (משרדים בבעלות מוסדיים — מגדל ביטוח והראל)
- חניון משותף בן 6 מפלסים, **2,400–2,800 מקומות חניה**
- מערכות נפרדות **ללא ממשקים ביניהן**:

| מערכת | תפקיד | אינטגרציה? |
|---|---|---|
| Visit (ויזיט) | CMMS — קריאות, משימות, מסמכים | — |
| Otello | בקרת מבנה (BMS) | אין |
| Wint | ניטור מים | אין |
| Priority | כספים, הזמנות רכש | אין |
```

**Key pattern:** Lead with who, what building, how big, then the systems table.
Always include the systems integration table when the interviewee manages multiple systems.

---

## Example: Pain Points Section (Nir Azulai Wix)

```markdown
## 3. חסרונות ונקודות כאב

### 3.1 כאבי תמחור ומודל עסקי
1. **מחיר פר-יוזר — רוצח לארגוני Enterprise.** ניר פותח בזה בשנייה הראשונה:
   "כשאתה מוכר לי תוכנה ואני צריך לשלם עליך פר-יוזר — זה כבר לא."

### 3.2 כאבי מדידה ואנליטיקס
3. **Visit לא מבין את הדאטה שלו עצמו.** זו הנקודה שניר הדגיש הכי חזק:
   "אין שם את ההבנה... ייקח עוד המון המון שנים."
4. **אין מדידת "קריאות מחזוריות".** ניר: "אני רוצה למדוד: מאיזה קריאות
   תיקנו פעם אחת, ואותה בעיה חזרה אחרי שבועיים?" —
   **זהו ה-KPI המרכזי ביותר, ואף מערכת לא מודדת אותו.**
```

**Key pattern:** Group pain points into themed sub-sections. Bold the core insight.
Integrate short quotes inline (don't save them only for the quotes section).

---

## Example: Opportunities Table (Nissim MyTower)

```markdown
## 6. הזדמנויות עבור BuildEye

> *הסעיף הבא הוא פרשנות של BuildEye, לא דברי הצד השני.*

| פער שזוהה | מה נאמר | הזדמנות ל-BuildEye |
|---|---|---|
| **תחזוקה מונעת על לוח+נעצים** | "לוח עם נעצים — כמו של פעם" | מודול משימות מחזוריות אוטומטי |
| **ידע מוסדי = סיכון אישי** | "מחר ניסים נוסע לחו"ל" | תיק נכס דיגיטלי שכולל ידע תפעולי |
| **BIM/תוכניות לא נגישות** | "לפתוח תוכנית — נדיר מאוד" | 2D floor plan click-to-ticket |
```

**Key pattern:** Always mark the opportunities table as BuildEye's analysis, not the
interviewee's words. Keep the "מה נאמר" column short (paraphrase, not full quote).

---

## Example: Key Quotes with Timestamps

```markdown
## 7. ציטוטים נבחרים עם חותמות זמן

1. **על מחיר פר-יוזר** (00:00:00):
   > *"כשאתה מוכר לי תוכנה ואני צריך לשלם עליך פר-יוזר — זה כבר לא."*

5. **על SLA ושעות עבודה** (01:04:37):
   > *"לא, אני עבדתי על זה 4–5 חודשים כדי לסדר את זה, וזה סודר בצורה עקומה."*

9. **על שבוע בלי מערכת** (01:27:46):
   > *"80 קריאות ביום × 7 ימים = 540 קריאות שהיית צריך לרשום ידנית... אין סיכוי."*
```

**How to find timestamps:** In the .srt file, segment N is at line 4*(N-1)+1.
Search for the quote text using Grep, note the surrounding segment numbers, then
read those lines of the .srt to get the timestamp. Always verify before writing.

---

## Example: 1-Page Executive Summary

```markdown
# סיכום חד-עמודי — ניסים, MyTower (מגורים), ניהול CBRE

**תאריך:** 28 באפריל 2026 | **אורך:** ~53 דקות | **מערכת:** MyTower

---

## מי הם המשתתפים
- **ניסים** — מנהל בניין MyTower (~200 דירות), 14 שנות ניסיון, גם גר בבניין
- **אלדד** — מנהל בכיר CBRE, מנהל נכסים מגורים ומסחריים

## על המערכת
- שתי אפליקציות: דייר + ניהול
- אפליקציית דייר: קריאות + תשלום שכר דירה + שירותי בניין
- **שביעות רצון גבוהה מאוד** — "לא מתקלט" (x3)

## פערים ובעיות
- **תחזוקה מונעת על לוח פיזי עם נעצים** — המודול קיים אך לא הופעל
- **MyTower ↔ Priority לא מחוברות** — בתהליך אינטגרציה
- **ועד הבית + מע"מ** — מבנה משפטי מורכב, אין כרטסת חשבונאית
```

**Key pattern:** Short, scannable, no quotes. Every bullet should be independently
meaningful — someone reading only this page should understand the core finding.
