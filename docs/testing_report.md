# SmartATS Testing Report

## Test environment

- macOS
- Python 3.12.13
- Pytest 9.1.1
- SBERT model: `all-MiniLM-L6-v2`
- spaCy model: `en_core_web_sm`

## Automated test command

```bash
python -m pytest -q
```

## Current result

```text
75 passed
```

## Tested areas

| Area | Examples |
|---|---|
| File validation | Valid extension, empty, oversized and unsupported files |
| Extraction | TXT, DOCX, corrupt PDF and low text |
| PDF layout | Automatic columns and layout-aware extraction |
| Text cleaning | Spaces, bullets, C++, C# and .NET |
| Sections | Standard, inline, additional and paragraph-only sections |
| Skills | Exact match, aliases, case and partial-word protection |
| Experience | Explicit years, date ranges and missing duration |
| Education | Bachelor, master and missing education |
| Semantic AI | Chunking, thresholds, evidence and project exclusion |
| Projects | Relevance, best two chunks and technology score |
| Final score | Weights, points, total and categories |
| Contacts | NER name, email, phone, ZIP rejection and title separation |
| CSV storage | Candidate, duplicate, score and evidence data |
| Dashboard | Charts and downloadable CSV |
| HR review | Stored details, status, notes and review history |

## Manual tests performed

- Single-column resume
- Multi-column resume with images
- Paragraph-style resume
- Resume section aliases
- Actual PDF contact row containing address, ZIP code, bullet and phone
- Saved-job reopening after Streamlit restart
- Dashboard filters and CSV download
- Candidate review update and timestamp history

## Known testing limitation

Automated tests use controlled sample text and matrices. Final model similarity can
vary when models or library versions change, so semantic tests validate ranges and
evidence logic rather than treating one model score as universal truth.

