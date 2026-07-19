# SmartATS

SmartATS is a beginner-friendly AI Resume Screening and Applicant Tracking
System. It compares resume evidence with a confirmed job description using
Sentence-BERT and transparent rule-based matching.

SmartATS supports HR review. It does not automatically hire or reject candidates.

## Main features

- PDF, DOCX and TXT resume upload
- Blank, corrupt, oversized and password-protected file handling
- Automatic single-column and multi-column PDF extraction
- Editable extracted-text preview
- Resume section detection and paragraph-only support
- Required and preferred skill matching with evidence
- Experience and education matching
- Related-project relevance using SBERT
- Requirement-level SBERT semantic evidence
- Fully explained weighted ATS score
- Candidate name, email and phone extraction
- Candidate CSV storage and duplicate detection
- HR dashboard, filters and Matplotlib charts
- Candidate details and timestamped HR review history
- Filtered CSV export

## Technology

- Python 3.12
- Streamlit
- Sentence Transformers using `all-MiniLM-L6-v2`
- spaCy using `en_core_web_sm`
- pypdf and pdfplumber
- python-docx
- Pandas and Matplotlib
- CSV files, Python dictionaries and lists
- Pytest

No JSON or SQL database is used.

## Installation on macOS

Open the SmartATS folder in VS Code and open a terminal.

Create a virtual environment:

```bash
python3.12 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install the spaCy English NER model:

```bash
python -m spacy download en_core_web_sm
```

## Run SmartATS

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` if the browser does not open automatically.

Stop the application with `Control + C`.

## Run automated tests

```bash
python -m pytest -q
```

## Application workflow

1. Create or reopen a job.
2. Confirm required skills, experience, education and scoring weights.
3. Upload one or more resumes.
4. Verify extracted text and detected sections.
5. Review skill, experience and education evidence.
6. Run SBERT semantic and project analysis.
7. Verify every final-score calculation.
8. Correct candidate contact details if necessary.
9. Save candidate results.
10. Compare candidates in the HR Dashboard.
11. Record the final human review in Candidate Details.

## Default scoring weights

| Component | Weight |
|---|---:|
| SBERT semantic similarity | 35% |
| Required skills | 35% |
| Related projects | 15% |
| Experience | 10% |
| Education | 5% |
| Total | 100% |

HR can change these weights during job setup. The saved job weights are applied
equally to every candidate screened for that job.

## Local data

Application data is stored locally in CSV files under `storage/`.

- `jobs.csv`
- `candidates.csv`
- `score_details.csv`
- `semantic_evidence.csv`
- `processing_errors.csv`
- `hr_reviews.csv`

Raw resume files and complete resume text are not stored permanently.

## Responsible use

Names, email addresses, phone numbers, photographs, addresses, age, gender,
religion, marital status and nationality are not used in scoring. A high score
means that written resume evidence aligns with the selected job configuration;
it does not prove candidate ability or future job performance.

Final hiring decisions must be made by qualified human reviewers.

## Documentation

- `docs/architecture.md`
- `docs/scoring_method.md`
- `docs/project_report.md`
- `docs/testing_report.md`
- `docs/presentation_notes.md`

