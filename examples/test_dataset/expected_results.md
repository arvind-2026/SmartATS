# SmartATS Five-Resume Test Dataset

## Job setup

Copy the contents of `job_description.txt` into SmartATS.

- Job title: Junior Python Backend Developer
- Required skills: Python, FastAPI, Flask, PostgreSQL, Git, Docker, REST API, Pytest
- Preferred skills: AWS, Redis, CI/CD, GitHub Actions
- Required experience: 2 years
- Required education: Bachelor's degree in Computer Science or related technical field
- Keep the default scoring weights.

## Expected qualitative order

Exact scores may vary slightly with model or library versions. Test the evidence and
relative ordering rather than expecting one fixed number.

| File | Layout test | Expected alignment | Main reason |
|---|---|---|---|
| `01_aisha_verma_classic_strong.pdf` | Classic single column | Highest / good match | All required skills, 3 years, relevant project and degree |
| `02_rohan_mehta_two_column_good.pdf` | Colored sidebar and main column | Second / good match | Most required skills, 2 years, relevant project and degree |
| `03_neha_singh_table_moderate.pdf` | Table-based skills | Middle / low match | Relevant junior skills but only 1 year and limited production tooling |
| `04_kabir_khan_paragraph_partial.pdf` | Paragraph-only resume | Lower / low match | Python evidence but little backend framework, database or deployment evidence |
| `05_meera_iyer_modern_cards_low.pdf` | Visual cards and decorative avatar | Low | Strong frontend/design background but weak alignment with backend role |

## What to verify

1. All five PDFs pass file validation.
2. Candidate names, emails and phone numbers are detected correctly.
3. The two-column and card layouts extract in a readable order.
4. The table resume preserves technical skills.
5. The paragraph resume uses paragraph-level analysis.
6. Missing skills are reported as not detected.
7. Project evidence comes only from project content.
8. The component arithmetic adds to the displayed overall score.
9. The dashboard ranks stronger document alignment above weaker alignment.
10. CSV export contains all five candidates and their contact details.

## Fictional data notice

All candidate identities and contact details in this dataset are fictional and are
created only for local SmartATS testing.
