# SmartATS TXT Test Dataset

## Job setup

Copy `job_description.txt` into SmartATS.

- Job title: Junior Frontend Developer
- Required skills: HTML, CSS, JavaScript, React, Git, REST API, Responsive Design, Jest
- Preferred skills: TypeScript, Redux, Figma
- Required experience: 2 years
- Required education: Bachelor's degree in Computer Science or a related technical field
- Keep the default scoring weights.

## Expected qualitative order

Exact SBERT scores can vary slightly by model or library version. Check the evidence
and relative ranking instead of expecting one fixed score.

| File | TXT structure test | Expected alignment | Main reason |
|---|---|---|---|
| `01_arjun_malhotra_classic_strong.txt` | Traditional headings and lists | Highest | All required skills, three years, relevant project and degree |
| `02_nisha_reddy_ascii_good.txt` | ASCII banner and bracket headings | Second | All required skills, two years and relevant project |
| `03_dev_singh_key_value_moderate.txt` | Key-value skill table | Middle | Relevant junior evidence but one year and testing gap |
| `04_farhan_ali_paragraph_partial.txt` | Paragraph-only narrative | Lower | Basic web-page evidence with limited application-development depth |
| `05_kavya_menon_minimal_low.txt` | Minimal short resume | Lowest | Customer-support background with weak frontend alignment |

## What to verify

1. All five TXT files pass validation.
2. UTF-8 text is extracted without corruption.
3. Candidate names, emails and phone numbers are detected correctly.
4. ASCII dividers and key-value rows do not prevent section detection.
5. The paragraph resume uses paragraph-level analysis.
6. Missing skills are shown as not detected.
7. Project evidence comes from project content.
8. Score arithmetic adds up to the displayed overall score.
9. The dashboard ranks stronger alignment above weaker alignment.
10. CSV export includes all five fictional candidates and their contact details.

## Fictional data notice

All candidate identities and contact details are fictional and exist only for local
SmartATS testing.
