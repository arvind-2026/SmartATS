from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.platypus import Table
from reportlab.platypus import TableStyle


OUTPUT_FOLDER = Path(__file__).parent
PAGE_WIDTH, PAGE_HEIGHT = letter
LEFT_MARGIN = 0.65 * inch
RIGHT_MARGIN = 0.65 * inch
TOP_MARGIN = 0.55 * inch
BOTTOM_MARGIN = 0.5 * inch

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#159A9C")
BLUE = colors.HexColor("#2D6CDF")
GREEN = colors.HexColor("#2E8B57")
ORANGE = colors.HexColor("#D97706")
PURPLE = colors.HexColor("#6D4AFF")
GRAY = colors.HexColor("#5F6B76")
LIGHT_GRAY = colors.HexColor("#EEF2F5")
DARK = colors.HexColor("#263442")


def wrap_lines(text, font_name, font_size, width):
    """Wrap text into lines that fit a fixed width."""

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        proposed_line = word if not current_line else current_line + " " + word

        if stringWidth(proposed_line, font_name, font_size) <= width:
            current_line = proposed_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_wrapped_text(
    pdf,
    text,
    x,
    y,
    width,
    font_name="Helvetica",
    font_size=9,
    leading=12,
    color=DARK,
    bullet=False,
):
    """Draw wrapped text and return the next vertical position."""

    bullet_indent = 10 if bullet else 0
    line_width = width - bullet_indent
    lines = wrap_lines(text, font_name, font_size, line_width)
    pdf.setFont(font_name, font_size)
    pdf.setFillColor(color)

    for index, line in enumerate(lines):
        line_x = x + bullet_indent

        if bullet and index == 0:
            pdf.drawString(x, y, "-")

        pdf.drawString(line_x, y, line)
        y -= leading

    return y


def draw_section_heading(pdf, title, x, y, width, accent=TEAL):
    """Draw a consistent section heading and return the next position."""

    pdf.setFillColor(accent)
    pdf.rect(x, y - 3, 4, 16, fill=1, stroke=0)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(x + 10, y, title)
    pdf.setStrokeColor(colors.HexColor("#CBD5DF"))
    pdf.line(x + 10, y - 5, x + width, y - 5)

    return y - 22


def save_pdf(pdf):
    """Finish one PDF file."""

    pdf.showPage()
    pdf.save()


def create_classic_resume():
    """Create a strong-match classic single-column resume."""

    file_path = OUTPUT_FOLDER / "01_aisha_verma_classic_strong.pdf"
    pdf = canvas.Canvas(str(file_path), pagesize=letter)
    usable_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    y = PAGE_HEIGHT - TOP_MARGIN

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 23)
    pdf.drawString(LEFT_MARGIN, y, "AISHA VERMA")
    y -= 20
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(LEFT_MARGIN, y, "PYTHON BACKEND DEVELOPER")
    y -= 18
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(
        LEFT_MARGIN,
        y,
        "+91 90000 10001 | aisha.verma@example.com | Pune, India | github.com/aishaverma",
    )
    y -= 23

    y = draw_section_heading(pdf, "PROFESSIONAL SUMMARY", LEFT_MARGIN, y, usable_width)
    y = draw_wrapped_text(
        pdf,
        "Python backend developer with 3 years of experience developing backend applications and "
        "REST APIs using Python, FastAPI and Flask. Strong experience with PostgreSQL, Git, Docker, "
        "Pytest, technical documentation and AWS.",
        LEFT_MARGIN,
        y,
        usable_width,
    )
    y -= 8

    y = draw_section_heading(pdf, "TECHNICAL SKILLS", LEFT_MARGIN, y, usable_width)
    skills = [
        "Languages: Python, SQL, Bash",
        "Frameworks: FastAPI, Flask, Django REST Framework",
        "Databases: PostgreSQL, MySQL, Redis",
        "Tools: Git, Docker, GitHub Actions, Pytest, Postman, AWS",
    ]
    for skill in skills:
        y = draw_wrapped_text(pdf, skill, LEFT_MARGIN, y, usable_width, bullet=True)
    y -= 5

    y = draw_section_heading(pdf, "PROFESSIONAL EXPERIENCE", LEFT_MARGIN, y, usable_width)
    pdf.setFillColor(DARK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(LEFT_MARGIN, y, "Backend Developer - CloudNova Systems")
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, y, "Jan 2023 - Present")
    y -= 15
    bullets = [
        "Built and maintained FastAPI REST services used by more than 20,000 monthly users.",
        "Optimized PostgreSQL queries and Redis caching, reducing API response time by 35 percent.",
        "Containerized services with Docker and added Pytest unit tests to the CI/CD pipeline.",
        "Collaborated through Git pull requests and deployed services to AWS.",
    ]
    for item in bullets:
        y = draw_wrapped_text(pdf, item, LEFT_MARGIN, y, usable_width, bullet=True)
    y -= 5

    y = draw_section_heading(pdf, "PROJECTS", LEFT_MARGIN, y, usable_width)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.setFillColor(DARK)
    pdf.drawString(LEFT_MARGIN, y, "Smart Inventory API")
    y -= 14
    y = draw_wrapped_text(
        pdf,
        "Developed backend applications and REST APIs using Python, FastAPI and Flask. Designed "
        "PostgreSQL data models and queries, wrote Pytest unit tests, used Git and Docker, and "
        "documented API decisions. Added Redis caching and GitHub Actions CI/CD deployment.",
        LEFT_MARGIN,
        y,
        usable_width,
        bullet=True,
    )
    y -= 5

    y = draw_section_heading(pdf, "EDUCATION", LEFT_MARGIN, y, usable_width)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.setFillColor(DARK)
    pdf.drawString(LEFT_MARGIN, y, "B.Tech in Computer Science - Pune Institute of Technology")
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, y, "2022")

    save_pdf(pdf)


def create_two_column_resume():
    """Create a good-match resume with a colored left sidebar."""

    file_path = OUTPUT_FOLDER / "02_rohan_mehta_two_column_good.pdf"
    pdf = canvas.Canvas(str(file_path), pagesize=letter)
    sidebar_width = 2.05 * inch
    main_x = sidebar_width + 0.35 * inch
    main_width = PAGE_WIDTH - main_x - RIGHT_MARGIN

    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, sidebar_width, PAGE_HEIGHT, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.circle(sidebar_width / 2, PAGE_HEIGHT - 0.85 * inch, 28, fill=0, stroke=1)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(sidebar_width / 2, PAGE_HEIGHT - 0.9 * inch, "RM")

    sidebar_y = PAGE_HEIGHT - 1.5 * inch
    for heading, body in [
        ("CONTACT", "rohan.mehta@example.com\n+91 90000 10002\nAhmedabad, India"),
        ("SKILLS", "Python\nFlask\nMySQL\nPostgreSQL\nGit\nDocker\nREST APIs\nPytest\nPostman"),
        ("LANGUAGES", "English\nHindi\nGujarati"),
    ]:
        pdf.setFillColor(TEAL)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(18, sidebar_y, heading)
        sidebar_y -= 15
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica", 8.5)

        for line in body.splitlines():
            pdf.drawString(18, sidebar_y, line)
            sidebar_y -= 13

        sidebar_y -= 15

    y = PAGE_HEIGHT - TOP_MARGIN
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(main_x, y, "ROHAN MEHTA")
    y -= 22
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(main_x, y, "BACKEND SOFTWARE ENGINEER")
    y -= 28

    y = draw_section_heading(pdf, "PROFILE", main_x, y, main_width)
    y = draw_wrapped_text(
        pdf,
        "Backend engineer with 2 years of experience creating Python and Flask services. "
        "Comfortable with PostgreSQL, MySQL, Git, Docker, Pytest and REST API testing.",
        main_x,
        y,
        main_width,
    )
    y -= 10

    y = draw_section_heading(pdf, "WORK EXPERIENCE", main_x, y, main_width)
    pdf.setFillColor(DARK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(main_x, y, "Python Developer - BrightLayer Labs")
    y -= 13
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 8.2)
    pdf.drawString(main_x, y, "Jul 2024 - Present")
    y -= 15
    for item in [
        "Developed Flask REST APIs and integrated PostgreSQL and MySQL databases.",
        "Used Docker for consistent local and test environments.",
        "Reviewed code through Git and wrote Pytest unit tests.",
    ]:
        y = draw_wrapped_text(pdf, item, main_x, y, main_width, bullet=True)
    y -= 12

    y = draw_section_heading(pdf, "PROJECT EXPERIENCE", main_x, y, main_width)
    pdf.setFillColor(DARK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(main_x, y, "Customer Support Ticket API")
    y -= 14
    y = draw_wrapped_text(
        pdf,
        "Built a Python Flask REST API with PostgreSQL for ticket creation, status tracking and "
        "role-based access. Packaged it with Docker, wrote Pytest tests and used Git for reviews.",
        main_x,
        y,
        main_width,
    )
    y -= 12

    y = draw_section_heading(pdf, "ACADEMIC BACKGROUND", main_x, y, main_width)
    y = draw_wrapped_text(
        pdf,
        "B.E. in Information Technology, Gujarat Technical University, 2024",
        main_x,
        y,
        main_width,
        font_name="Helvetica-Bold",
    )

    save_pdf(pdf)


def create_table_resume():
    """Create a moderate-match resume using tables and boxed sections."""

    file_path = OUTPUT_FOLDER / "03_neha_singh_table_moderate.pdf"
    pdf = canvas.Canvas(str(file_path), pagesize=letter)
    usable_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

    pdf.setFillColor(BLUE)
    pdf.rect(0, PAGE_HEIGHT - 1.15 * inch, PAGE_WIDTH, 1.15 * inch, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(LEFT_MARGIN, PAGE_HEIGHT - 0.55 * inch, "NEHA SINGH")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(LEFT_MARGIN, PAGE_HEIGHT - 0.82 * inch, "JUNIOR SOFTWARE DEVELOPER")
    pdf.drawRightString(
        PAGE_WIDTH - RIGHT_MARGIN,
        PAGE_HEIGHT - 0.55 * inch,
        "neha.singh@example.com",
    )
    pdf.drawRightString(
        PAGE_WIDTH - RIGHT_MARGIN,
        PAGE_HEIGHT - 0.78 * inch,
        "+91 90000 10003",
    )

    y = PAGE_HEIGHT - 1.45 * inch
    y = draw_section_heading(pdf, "CAREER OBJECTIVE", LEFT_MARGIN, y, usable_width, BLUE)
    y = draw_wrapped_text(
        pdf,
        "Junior developer seeking a Python backend role. One year of internship experience with "
        "Django, SQLite, Git and basic REST API development.",
        LEFT_MARGIN,
        y,
        usable_width,
    )
    y -= 10

    y = draw_section_heading(pdf, "TECHNICAL PROFICIENCY", LEFT_MARGIN, y, usable_width, BLUE)
    styles = getSampleStyleSheet()
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
    )
    table_data = [
        ["Category", "Knowledge"],
        ["Programming", Paragraph("Python, SQL, JavaScript", cell_style)],
        ["Frameworks", Paragraph("Django, Django REST Framework", cell_style)],
        ["Database", Paragraph("SQLite, basic PostgreSQL", cell_style)],
        ["Tools", Paragraph("Git, GitHub, Docker, Postman", cell_style)],
    ]
    table = Table(table_data, colWidths=[1.35 * inch, usable_width - 1.35 * inch])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C5D6")),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F6F9FC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )
    table_width, table_height = table.wrapOn(pdf, usable_width, PAGE_HEIGHT)
    table.drawOn(pdf, LEFT_MARGIN, y - table_height)
    y -= table_height + 18

    y = draw_section_heading(pdf, "EMPLOYMENT HISTORY", LEFT_MARGIN, y, usable_width, BLUE)
    pdf.setFillColor(DARK)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(LEFT_MARGIN, y, "Software Development Intern - CodeBridge Academy")
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, y, "Jun 2025 - Jun 2026")
    y -= 15
    for item in [
        "Created Django views and REST endpoints for an internal learning portal.",
        "Worked with SQLite and wrote basic SQL queries and unit tests.",
        "Used Git branches and pull requests for team collaboration.",
    ]:
        y = draw_wrapped_text(pdf, item, LEFT_MARGIN, y, usable_width, bullet=True)
    y -= 8

    y = draw_section_heading(pdf, "ACADEMIC PROJECTS", LEFT_MARGIN, y, usable_width, BLUE)
    y = draw_wrapped_text(
        pdf,
        "Library Management Portal - Developed a Django and SQLite REST application for book "
        "search, issue tracking and user login. Packaged the project with basic Docker settings.",
        LEFT_MARGIN,
        y,
        usable_width,
        bullet=True,
    )
    y -= 8

    y = draw_section_heading(pdf, "QUALIFICATIONS", LEFT_MARGIN, y, usable_width, BLUE)
    y = draw_wrapped_text(
        pdf,
        "BCA, National College of Computing, 2025",
        LEFT_MARGIN,
        y,
        usable_width,
        font_name="Helvetica-Bold",
    )

    save_pdf(pdf)


def create_paragraph_resume():
    """Create a partial-match resume written mostly as paragraphs."""

    file_path = OUTPUT_FOLDER / "04_kabir_khan_paragraph_partial.pdf"
    pdf = canvas.Canvas(str(file_path), pagesize=letter)
    usable_width = PAGE_WIDTH - 1.2 * inch
    x = 0.6 * inch
    y = PAGE_HEIGHT - 0.65 * inch

    pdf.setFillColor(DARK)
    pdf.setFont("Times-Bold", 24)
    pdf.drawCentredString(PAGE_WIDTH / 2, y, "Kabir Khan")
    y -= 20
    pdf.setFont("Times-Italic", 10)
    pdf.setFillColor(GRAY)
    pdf.drawCentredString(
        PAGE_WIDTH / 2,
        y,
        "kabir.khan@example.com  |  +91 90000 10004  |  Lucknow, India",
    )
    y -= 28
    pdf.setStrokeColor(ORANGE)
    pdf.setLineWidth(2)
    pdf.line(x, y, PAGE_WIDTH - x, y)
    y -= 28

    paragraphs = [
        "I am an early-career programmer with approximately 1 year of internship and freelance "
        "experience. I mainly use Python for automation scripts, CSV processing and small data "
        "analysis tasks with pandas. I have also used Git for personal repositories.",
        "During my internship at NorthStar Services from July 2025 to June 2026, I automated "
        "weekly spreadsheet reports and cleaned customer data using Python. I wrote simple SQL "
        "queries for SQLite but did not work on production web APIs or cloud deployments.",
        "For a personal expense tracker, I wrote a command-line Python program that imports bank "
        "transactions from CSV files and creates monthly summaries with pandas and Matplotlib. "
        "The project is a local command-line tool without a web framework, production database "
        "or container deployment.",
        "I completed a B.A. in Economics from Avadh University in 2025. I am currently learning "
        "backend development, REST concepts and software testing through online courses.",
        "My strengths include careful documentation, communication and willingness to learn. "
        "I speak English, Hindi and Urdu and enjoy reading technology articles.",
    ]

    for paragraph in paragraphs:
        y = draw_wrapped_text(
            pdf,
            paragraph,
            x,
            y,
            usable_width,
            font_name="Times-Roman",
            font_size=11,
            leading=16,
            color=DARK,
        )
        y -= 17

    pdf.setFillColor(ORANGE)
    pdf.rect(x, BOTTOM_MARGIN, usable_width, 0.08 * inch, fill=1, stroke=0)

    save_pdf(pdf)


def create_modern_cards_resume():
    """Create a low-match visual card-style resume."""

    file_path = OUTPUT_FOLDER / "05_meera_iyer_modern_cards_low.pdf"
    pdf = canvas.Canvas(str(file_path), pagesize=letter)
    pdf.setFillColor(colors.HexColor("#F7F5FF"))
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    pdf.setFillColor(PURPLE)
    pdf.circle(0.82 * inch, PAGE_HEIGHT - 0.82 * inch, 31, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawCentredString(0.82 * inch, PAGE_HEIGHT - 0.88 * inch, "MI")

    pdf.setFillColor(DARK)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(1.35 * inch, PAGE_HEIGHT - 0.67 * inch, "MEERA IYER")
    pdf.setFillColor(PURPLE)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(1.35 * inch, PAGE_HEIGHT - 0.92 * inch, "UI DESIGNER AND FRONTEND SPECIALIST")
    pdf.setFillColor(GRAY)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(
        PAGE_WIDTH - 0.55 * inch,
        PAGE_HEIGHT - 0.7 * inch,
        "meera.iyer@example.com",
    )
    pdf.drawRightString(
        PAGE_WIDTH - 0.55 * inch,
        PAGE_HEIGHT - 0.9 * inch,
        "+91 90000 10005",
    )

    cards = [
        (
            "PROFILE",
            "Creative UI designer with 3 years of experience producing accessible websites, "
            "design systems and interactive prototypes for consumer brands.",
            0.55 * inch,
            PAGE_HEIGHT - 2.0 * inch,
            3.25 * inch,
            1.05 * inch,
        ),
        (
            "CORE SKILLS",
            "Figma, Adobe XD, HTML5, CSS3, JavaScript, React, responsive design, user research",
            3.95 * inch,
            PAGE_HEIGHT - 2.0 * inch,
            3.95 * inch,
            1.05 * inch,
        ),
        (
            "CAREER HISTORY",
            "UI Designer - PixelCraft Studio | Jan 2023 - Present\nDesigned responsive interfaces, "
            "maintained a React component library and conducted usability testing. Collaborated "
            "with developers but did not build backend APIs or database services.",
            0.55 * inch,
            PAGE_HEIGHT - 4.2 * inch,
            7.35 * inch,
            1.85 * inch,
        ),
        (
            "SELECTED PROJECT",
            "Travel Booking Interface - Created a Figma prototype and React front end for hotel "
            "search and booking. Focused on accessibility, typography and responsive layouts.",
            0.55 * inch,
            PAGE_HEIGHT - 5.75 * inch,
            4.55 * inch,
            1.25 * inch,
        ),
        (
            "EDUCATION",
            "Bachelor of Design, National Institute of Design, 2022",
            5.25 * inch,
            PAGE_HEIGHT - 5.75 * inch,
            2.65 * inch,
            1.25 * inch,
        ),
        (
            "ACHIEVEMENTS",
            "Won a regional interface design award and led an accessibility workshop for 40 students.",
            0.55 * inch,
            PAGE_HEIGHT - 7.05 * inch,
            3.55 * inch,
            0.95 * inch,
        ),
        (
            "INTERESTS",
            "Typography, illustration, travel photography and inclusive design",
            4.25 * inch,
            PAGE_HEIGHT - 7.05 * inch,
            3.65 * inch,
            0.95 * inch,
        ),
    ]

    styles = getSampleStyleSheet()

    for title, body, x, top, width, height in cards:
        pdf.setFillColor(colors.white)
        pdf.roundRect(x, top - height, width, height, 9, fill=1, stroke=0)
        pdf.setFillColor(PURPLE)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(x + 12, top - 18, title)
        body_style = ParagraphStyle(
            title,
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=DARK,
            alignment=TA_CENTER if title == "EDUCATION" else 0,
        )
        paragraph = Paragraph(body.replace("\n", "<br/>"), body_style)
        paragraph_width, paragraph_height = paragraph.wrapOn(
            pdf,
            width - 24,
            height - 34,
        )
        paragraph_y = top - 32 - paragraph_height
        paragraph.drawOn(pdf, x + 12, paragraph_y)

    save_pdf(pdf)


def main():
    """Generate all five test resume PDFs."""

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    create_classic_resume()
    create_two_column_resume()
    create_table_resume()
    create_paragraph_resume()
    create_modern_cards_resume()
    print("Created five SmartATS test resume PDFs in", OUTPUT_FOLDER)


if __name__ == "__main__":
    main()
