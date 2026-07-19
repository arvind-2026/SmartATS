# SmartATS Project Report

## Project title

SmartATS: Explainable AI Resume Screening and Applicant Tracking System

## Problem statement

HR teams may receive many resumes for one job. Manual comparison is time-consuming,
while basic keyword systems can miss related meaning and unexplained AI scores can
reduce trust. SmartATS provides structured, explainable resume-to-job comparison.

## Objectives

- Accept common resume file formats.
- handle simple, multi-column and paragraph resumes.
- identify skills, projects, experience and education.
- use SBERT for semantic comparison.
- explain every awarded score point.
- provide an HR dashboard and CSV export.
- keep the final decision under human control.

## Methodology

SmartATS first validates and extracts resume text. It cleans the text, detects
sections and applies rule-based matching for structured requirements. SBERT creates
embeddings for semantic comparison. The five component percentages are combined
with job-specific weights. Evidence, calculations and warnings are displayed before
candidate results are saved locally.

## Input

- Job title and description
- Required and preferred skills
- Minimum experience
- Required education
- Scoring weights
- PDF, DOCX or TXT resumes

## Output

- Overall ATS score and match category
- Component score breakdown
- Matched and missing skills
- Related project evidence
- Experience and education evidence
- Job requirement to resume sentence matches
- Candidate ranking and dashboard charts
- CSV reports and HR review history

## AI concepts demonstrated

- Natural language processing
- Named entity recognition
- Sentence embeddings
- Cosine similarity
- Threshold-based classification
- Explainable AI evidence
- Human-in-the-loop decision support

## Ethical considerations

Sensitive personal information is excluded from scoring. SmartATS does not make an
automatic hiring decision. Scores reflect only written document alignment and may
be affected by resume quality, extraction accuracy, omitted information or model
limitations. HR must verify evidence and conduct an independent selection process.

## Conclusion

SmartATS demonstrates how semantic AI can improve resume-to-job comparison while
remaining transparent. Its modular beginner-friendly code, local CSV storage,
automated tests and HR evidence screens make it suitable as a Foundation of AI
project and as a base for future development.

## Future scope

- OCR for scanned resumes
- Multilingual models
- Secure authentication and access control
- Advanced overlapping-date calculation
- Anonymised initial review mode
- Deployment with encrypted persistent storage
- Integration with job portals and interview scheduling

