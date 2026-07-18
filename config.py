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


# SBERT settings
SBERT_MODEL_NAME = "all-MiniLM-L6-v2"
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


# Overall score categories
STRONG_SCORE_LIMIT = 80
GOOD_SCORE_LIMIT = 65
PARTIAL_SCORE_LIMIT = 50


# Project scoring settings
MAX_PROJECTS_FOR_SCORING = 2
PROJECT_RELEVANCE_POINTS = 10
PROJECT_TECHNOLOGY_POINTS = 5


# Dashboard settings
CHART_COLOR_PRIMARY = "#2563EB"
CHART_COLOR_SUCCESS = "#16A34A"
CHART_COLOR_WARNING = "#F59E0B"
CHART_COLOR_DANGER = "#DC2626"
CHART_WIDTH = 10
CHART_HEIGHT = 6
MAX_CANDIDATES_IN_CHART = 10

REVIEW_STATUSES = [
    "Not reviewed",
    "Shortlisted",
    "Needs review",
    "Not selected",
]


# User messages
RESPONSIBLE_AI_MESSAGE = (
    "SmartATS supports human review. It does not automatically hire or reject candidates."
)
INVALID_FILE_MESSAGE = "Please upload a PDF, DOCX, or TXT file."
EMPTY_FILE_MESSAGE = "The uploaded file is empty."
CORRUPT_FILE_MESSAGE = "The file is damaged or cannot be read."
SCANNED_FILE_MESSAGE = "This may be a scanned PDF that requires OCR."
LOW_TEXT_MESSAGE = "Only a small amount of readable text was found."

