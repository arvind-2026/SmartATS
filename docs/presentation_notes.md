# Presentation Notes

## Slide 1: Title

SmartATS: Explainable AI Resume Screening and Applicant Tracking System

Introduce the problem: HR must compare many resumes with one job description.

## Slide 2: Problem

- Manual screening takes time.
- Keyword matching misses related meaning.
- Black-box scores are difficult to trust.
- Poor extraction can create misleading results.

## Slide 3: Objectives

- Process PDF, DOCX and TXT resumes.
- Support different layouts.
- Compare skills and semantic meaning.
- include relevant candidate projects.
- explain every score.
- provide HR visualisation and export.

## Slide 4: Architecture

Explain the flow from job setup to extraction, analysis, score, storage and dashboard.
Emphasise that UI code and processing code are separated into different folders.

## Slide 5: AI concepts

Explain embeddings as numerical representations of sentence meaning. Explain cosine
similarity as a measurement of direction similarity between two embedding vectors.
Explain spaCy NER as detecting a person-name entity.

## Slide 6: Scoring

Show the five default weights and one manual calculation. Explain that HR confirms
weights before screening and every candidate for that job uses the same weights.

## Slide 7: Explainability

Demonstrate a job requirement, its best resume evidence, similarity, skill evidence
and final arithmetic. Use the phrase: no score without calculation and evidence.

## Slide 8: HR Dashboard

Show ranking, filters, component comparison, skill availability and CSV export.
Explain that HR sees trade-offs instead of relying only on rank.

## Slide 9: Validation and testing

Show the passing test count. Mention corrupt files, multi-column PDF, paragraph
resume, contact extraction, skill aliases, score arithmetic and CSV storage.

## Slide 10: Ethics and limitations

Explain that personal identity does not affect scoring, missing written evidence is
not proof of missing ability, and the system does not automatically reject anyone.

## Slide 11: Demonstration order

1. Create a job.
2. Upload a resume.
3. Show extracted text and sections.
4. Show structured evidence.
5. Run SBERT.
6. Explain final arithmetic.
7. Save candidate.
8. Open dashboard and candidate details.

## Slide 12: Conclusion and future scope

Summarise transparent AI decision support. Mention OCR, multilingual support,
authentication, anonymised review and secure deployment as future improvements.

## Likely questions

### Why use SBERT instead of keywords only?

SBERT can recognise related meaning when the job and resume use different wording.

### Does the highest score mean the best candidate?

No. It means the written resume aligns strongly with the configured job. HR must
verify ability through interviews and other selection methods.

### How is bias reduced?

Personal identity fields are excluded from scoring, rules are consistent for one
job, evidence is visible and final decisions remain human.

### What happens with a scanned PDF?

SmartATS warns that readable text was not found and does not create a misleading
score. OCR is future scope.

### Where is the data stored?

Structured results are stored locally in CSV files. Raw resume files and complete
resume text are not stored permanently.

