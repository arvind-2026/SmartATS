# SmartATS DOCX Test Dataset

## Job setup

Copy `job_description.txt` into SmartATS.

- Job title: Junior Data Analyst
- Required skills: Python, SQL, Microsoft Excel, Power BI, pandas, Data Visualization, Statistics, Git
- Preferred skills: Tableau, NumPy, scikit-learn
- Required experience: 2 years
- Required education: Bachelor's degree in a quantitative or related field
- Keep the default scoring weights.

## Expected qualitative order

Exact SBERT scores can vary slightly by model or library version. Check the evidence
and relative ranking instead of expecting one fixed score.

| File | DOCX layout test | Expected alignment | Main reason |
|---|---|---|---|
| `01_ananya_sharma_classic_strong.docx` | Classic one-column headings and bullets | Highest | All required skills, three years, relevant project and degree |
| `02_vikram_patel_sidebar_good.docx` | Colored sidebar with main content | Second | Most required skills, two years and relevant dashboard project |
| `03_sana_khan_skills_table_moderate.docx` | Genuine skills table | Middle | Relevant junior skills but only one year and some tool gaps |
| `04_rahul_das_paragraph_partial.docx` | Paragraph-only narrative | Lower | Some Excel, SQL and reporting evidence but limited BI tooling |
| `05_priya_nair_modern_cards_low.docx` | Modern card-style blocks | Lowest | Marketing background with weak data-analysis alignment |

## What to verify

1. All five DOCX files pass validation.
2. Candidate names, emails and phone numbers are detected correctly.
3. Paragraphs and table-cell text are both extracted.
4. The sidebar and modern-card documents remain readable after extraction.
5. The paragraph resume uses paragraph-level analysis.
6. Missing skills are reported as not detected.
7. Project evidence comes from the project content.
8. The score explanation adds up to the displayed overall score.
9. The dashboard ranks stronger job alignment above weaker alignment.
10. CSV export includes all five fictional candidates and their contact details.

## Fictional data notice

All candidate identities and contact details are fictional and exist only for local
SmartATS testing.

