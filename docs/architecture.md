# SmartATS Architecture

## Design goal

SmartATS uses small Python modules with one clear purpose. Streamlit pages handle
user interaction, while modules handle validation, extraction, matching, scoring,
charts and CSV storage.

## Data flow

```text
Job setup
    -> resume upload
    -> file validation
    -> PDF, DOCX or TXT extraction
    -> extraction quality check
    -> text cleaning
    -> section detection
    -> skill, experience and education matching
    -> SBERT semantic and project matching
    -> weighted score calculation
    -> evidence explanation
    -> candidate CSV storage
    -> HR dashboard and candidate review
```

## Main folders

```text
SmartATS/
├── app.py                 Home page
├── config.py              All application settings
├── pages/                 Streamlit screens
├── modules/               Reusable processing functions
├── data/                  Editable reference CSV files
├── storage/               Local application CSV files
├── exports/               Generated exports
├── tests/                 Automated tests
└── docs/                  Project documentation
```

## Streamlit pages

- `1_Job_Setup.py`: creates and reopens job configurations.
- `2_Upload_Resumes.py`: validates, extracts and analyses resumes.
- `3_HR_Dashboard.py`: ranks, filters, visualises and exports candidates.
- `4_Candidate_Details.py`: displays stored evidence and saves HR reviews.
- `5_About_SmartATS.py`: explains the AI, scoring, privacy and limitations.

## Core modules

| Module | Responsibility |
|---|---|
| `file_validator.py` | File type, size and batch validation |
| `resume_extractor.py` | PDF, DOCX and TXT extraction |
| `text_cleaner.py` | Spacing, bullets and analysis text |
| `section_detector.py` | Resume heading and paragraph detection |
| `skill_matcher.py` | Skills, aliases and exact evidence |
| `experience_matcher.py` | Duration and employment-date matching |
| `education_matcher.py` | Education terminology and levels |
| `semantic_matcher.py` | Requirement-level SBERT comparison |
| `project_matcher.py` | Project relevance and technologies |
| `score_calculator.py` | Weighted final-score arithmetic |
| `explanation_builder.py` | HR-readable formulas |
| `contact_extractor.py` | Name NER, email and phone extraction |
| `csv_manager.py` | Persistent local data and review history |
| `chart_maker.py` | Matplotlib dashboard charts |
| `csv_exporter.py` | Downloadable candidate report |

## Data representation

One job or candidate is represented by a Python dictionary. Multiple records are
stored in Python lists. Streamlit session state holds temporary running data, and
CSV files provide permanent local storage.

## AI architecture

SBERT uses `all-MiniLM-L6-v2` to encode requirements and resume sentences as
embeddings. Cosine similarity compares their semantic meaning. The strongest
resume sentence is retained as evidence for each job requirement.

Project text is excluded from general semantic matching because projects receive
a separate score. This reduces duplicate rewards.

spaCy NER helps detect candidate names. Contact details are editable and are used
only for candidate identification, never scoring.

## Explainability

Every component stores its raw percentage, job weight, awarded points and formula.
Semantic evidence stores the job requirement, resume sentence and similarity.
HR can verify extracted text before analysis and review stored evidence afterward.

