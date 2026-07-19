from pathlib import Path


# Application settings
APP_NAME = "SmartATS"
APP_SUBTITLE = "AI Resume Screening and Applicant Tracking System"
APP_DESCRIPTION = "Compare resumes with a job description using explainable AI."
APP_VERSION = "1.0.0"
PAGE_TITLE = "SmartATS"
PAGE_ICON = "📄"
PAGE_LAYOUT = "wide"


# Project paths
PROJECT_FOLDER = Path(__file__).parent
DATA_FOLDER = PROJECT_FOLDER / "data"
STORAGE_FOLDER = PROJECT_FOLDER / "storage"
EXPORT_FOLDER = PROJECT_FOLDER / "exports"

SKILLS_FILE = DATA_FOLDER / "skills.csv"
SKILL_ALIASES_FILE = DATA_FOLDER / "skill_aliases.csv"
EDUCATION_TERMS_FILE = DATA_FOLDER / "education_terms.csv"

JOBS_FILE = STORAGE_FOLDER / "jobs.csv"
CANDIDATES_FILE = STORAGE_FOLDER / "candidates.csv"
SCORE_DETAILS_FILE = STORAGE_FOLDER / "score_details.csv"
SEMANTIC_EVIDENCE_FILE = STORAGE_FOLDER / "semantic_evidence.csv"
PROCESSING_ERRORS_FILE = STORAGE_FOLDER / "processing_errors.csv"
HR_REVIEWS_FILE = STORAGE_FOLDER / "hr_reviews.csv"


# Resume file settings
ALLOWED_FILE_TYPES = ["pdf", "docx", "txt"]
MAX_FILE_SIZE_MB = 5
MINIMUM_TEXT_LENGTH = 100
MAX_FILES_PER_BATCH = 50
BYTES_PER_MB = 1024 * 1024
FILE_NAME_SEPARATOR = "."
TEXT_ENCODINGS = ["utf-8", "latin-1"]
TEXT_PREVIEW_HEIGHT = 250
PDF_FONT_LOGGER_NAME = "pdfminer.pdffont"
PDF_FONT_LOG_LEVEL = "ERROR"
MINIMUM_COLUMN_SPLIT_PERCENT = 25
MAXIMUM_COLUMN_SPLIT_PERCENT = 75
COLUMN_SCAN_STEP_PERCENT = 2
PERCENT_DIVISOR = 100
MINIMUM_WORDS_FOR_COLUMN_CHECK = 20
MINIMUM_WORDS_PER_COLUMN_PERCENT = 20
GUTTER_CHECK_WIDTH_PERCENT = 2
MAXIMUM_GUTTER_WORD_PERCENT = 4
MAXIMUM_CROSSING_WORD_PERCENT = 2
MAXIMUM_BLANK_LINES = 1


# SBERT settings
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"
NAME_NER_MODEL = "en_core_web_sm"
PERSON_ENTITY_LABEL = "PERSON"
NAME_SCAN_LINE_LIMIT = 8
NAME_SCAN_CHARACTER_LIMIT = 500
MINIMUM_NAME_WORDS = 2
MAXIMUM_NAME_WORDS = 5
MINIMUM_PHONE_DIGITS = 7
MAXIMUM_PHONE_DIGITS = 15
CONTACT_LINE_LABELS = ["phone", "mobile", "contact", "tel", "cell"]
CONTACT_SEGMENT_SEPARATORS = ["•", "●", "▪", "|"]
NAME_ROLE_WORDS = [
    "developer",
    "engineer",
    "manager",
    "analyst",
    "designer",
    "consultant",
    "intern",
    "junior",
    "senior",
]
NO_MATCH_LIMIT = 0.40
WEAK_MATCH_LIMIT = 0.60
STRONG_MATCH_LIMIT = 0.75


# Default scoring weights
DEFAULT_SEMANTIC_WEIGHT = 35
DEFAULT_SKILL_WEIGHT = 35
DEFAULT_PROJECT_WEIGHT = 15
DEFAULT_EXPERIENCE_WEIGHT = 10
DEFAULT_EDUCATION_WEIGHT = 5
TOTAL_SCORE_WEIGHT = 100

SCORE_COMPONENTS = [
    {
        "key": "semantic",
        "label": "Semantic similarity",
        "weight_key": "semantic_weight",
    },
    {
        "key": "skills",
        "label": "Required skills",
        "weight_key": "skill_weight",
    },
    {
        "key": "projects",
        "label": "Related projects",
        "weight_key": "project_weight",
    },
    {
        "key": "experience",
        "label": "Experience",
        "weight_key": "experience_weight",
    },
    {
        "key": "education",
        "label": "Education",
        "weight_key": "education_weight",
    },
]


# Overall score categories
STRONG_SCORE_LIMIT = 80
GOOD_SCORE_LIMIT = 65
PARTIAL_SCORE_LIMIT = 50

STRONG_SCORE_LABEL = "Strong match"
GOOD_SCORE_LABEL = "Good match"
PARTIAL_SCORE_LABEL = "Partial match"
LOW_SCORE_LABEL = "Low match"


# Project scoring settings
MAX_PROJECTS_FOR_SCORING = 2
PROJECT_RELEVANCE_POINTS = 10
PROJECT_TECHNOLOGY_POINTS = 5
PROJECT_COMPONENT_POINTS = PROJECT_RELEVANCE_POINTS + PROJECT_TECHNOLOGY_POINTS


# Dashboard settings
CHART_COLOR_PRIMARY = "#2563EB"
CHART_COLOR_SUCCESS = "#16A34A"
CHART_COLOR_WARNING = "#F59E0B"
CHART_COLOR_DANGER = "#DC2626"
MATPLOTLIB_BACKEND = "Agg"
CHART_WIDTH = 10
CHART_HEIGHT = 6
MAX_CANDIDATES_IN_CHART = 10
ALL_FILTER_OPTION = "All"
MINIMUM_DASHBOARD_SCORE = 0
MAXIMUM_DASHBOARD_SCORE = 100
DASHBOARD_SCORE_STEP = 5
CSV_EXPORT_FILE_NAME = "candidate_ranking.csv"

DASHBOARD_SCORE_FIELDS = [
    "semantic_score",
    "skill_score",
    "project_score",
    "experience_score",
    "education_score",
    "overall_score",
]

DASHBOARD_TABLE_COLUMNS = [
    "rank",
    "candidate_id",
    "candidate_name",
    "candidate_email",
    "candidate_phone",
    "overall_score",
    "semantic_score",
    "skill_score",
    "project_score",
    "experience_score",
    "education_score",
    "matched_skills",
    "missing_skills",
    "extraction_quality",
    "review_status",
]

REVIEW_STATUSES = [
    "Not reviewed",
    "Shortlisted",
    "Needs review",
    "Not selected",
]


# Resume section names and common heading alternatives
SECTION_HEADINGS = {
    "summary": [
        "summary",
        "profile",
        "professional summary",
        "career objective",
        "objective",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "competencies",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
    ],
    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "courses",
        "training",
    ],
    "achievements": [
        "achievements",
        "awards",
        "awards and achievements",
        "honours",
        "honors",
    ],
    "languages": [
        "languages",
        "language proficiency",
        "known languages",
    ],
    "strengths": [
        "strengths",
        "key strengths",
        "personal strengths",
    ],
    "interests": [
        "interests",
        "areas of interest",
        "hobbies and interests",
        "hobbies",
    ],
}


# Job form settings
JOB_ID_PREFIX = "JOB"
JOB_ID_DIGITS = 3
CANDIDATE_ID_PREFIX = "CAN"
CANDIDATE_ID_DIGITS = 3
MINIMUM_JOB_DESCRIPTION_LENGTH = 50
SKILL_SEPARATOR = ","
EVIDENCE_SENTENCE_SEPARATORS = ["\n", ".", ";"]
MONTHS_PER_YEAR = 12
ROUND_SCORE_DIGITS = 2
MINIMUM_REQUIREMENT_LENGTH = 20
MINIMUM_RESUME_CHUNK_LENGTH = 15
MAXIMUM_JOB_REQUIREMENTS = 20
MAXIMUM_RESUME_CHUNKS = 150
MAXIMUM_PROJECT_CHUNKS = 30
SEMANTIC_EXCLUDED_SECTIONS = ["projects"]
SBERT_PROGRESS_BAR = False

MONTH_NAMES = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

EDUCATION_LEVELS = [
    "school",
    "diploma",
    "bachelor",
    "master",
    "doctorate",
]

JOB_CSV_HEADERS = [
    "job_id",
    "job_title",
    "job_description",
    "required_skills",
    "preferred_skills",
    "required_experience",
    "required_education",
    "semantic_weight",
    "skill_weight",
    "project_weight",
    "experience_weight",
    "education_weight",
]

CANDIDATE_CSV_HEADERS = [
    "candidate_id",
    "job_id",
    "candidate_name",
    "candidate_email",
    "candidate_phone",
    "file_name",
    "semantic_score",
    "skill_score",
    "project_score",
    "experience_score",
    "education_score",
    "overall_score",
    "matched_skills",
    "missing_skills",
    "extraction_quality",
    "review_status",
    "hr_notes",
]

SCORE_DETAIL_CSV_HEADERS = [
    "candidate_id",
    "component",
    "match_percentage",
    "weight",
    "points_awarded",
    "calculation",
]

SEMANTIC_EVIDENCE_CSV_HEADERS = [
    "candidate_id",
    "job_requirement",
    "resume_evidence",
    "similarity",
]

HR_REVIEW_CSV_HEADERS = [
    "candidate_id",
    "review_status",
    "hr_notes",
    "reviewed_at",
]

REVIEW_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# User messages
RESPONSIBLE_AI_MESSAGE = (
    "SmartATS supports human review. It does not automatically hire or reject candidates."
)
INVALID_FILE_MESSAGE = "Please upload a PDF, DOCX, or TXT file."
EMPTY_FILE_MESSAGE = "The uploaded file is empty."
CORRUPT_FILE_MESSAGE = "The file is damaged or cannot be read."
SCANNED_FILE_MESSAGE = "This may be a scanned PDF that requires OCR."
LOW_TEXT_MESSAGE = "Only a small amount of readable text was found."
TOO_LARGE_FILE_MESSAGE = "The uploaded file is larger than the allowed limit."
TOO_MANY_FILES_MESSAGE = "Too many resumes were uploaded at one time."
PASSWORD_FILE_MESSAGE = "The PDF is password-protected. Please upload an unlocked copy."
EXTRACTION_SUCCESS_MESSAGE = "Resume text extracted successfully."
MODEL_LOADING_MESSAGE = "Loading the SBERT model and comparing semantic meaning..."
NAME_MODEL_MESSAGE = (
    "The name NER model is unavailable. A low-confidence fallback name was used."
)
