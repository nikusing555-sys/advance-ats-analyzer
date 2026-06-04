from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


def generate_resume_pdf(
    filename,
    name,
    email,
    phone,
    linkedin,
    content
):

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=8
    )

    contact_style = ParagraphStyle(
        "ContactStyle",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=12
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        textColor=colors.black,
        fontSize=13,
        leading=16,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14
    )

    story = []

    # ======================
    # HEADER
    # ======================

    story.append(
        Paragraph(
            name.upper(),
            name_style
        )
    )

    story.append(
        Paragraph(
            f"{email} | {phone}",
            contact_style
        )
    )

    if linkedin:
        story.append(
            Paragraph(
                linkedin,
                contact_style
            )
        )

    story.append(
        Spacer(1, 15)
    )

    # ======================
    # CLEAN AI RESPONSE
    # ======================

    content = content.replace("###", "")
    content = content.replace("##", "")
    content = content.replace("#", "")
    content = content.replace("**", "")
    content = content.replace("---", "")

    content = content.replace(
        "Certainly! Below is a professionally rewritten version of the resume:",
        ""
    )

    content = content.replace(
        "Certainly! Here's the rewritten resume:",
        ""
    )

    content = content.replace(
        "Here is the rewritten resume:",
        ""
    )

    section_headers = [
        "CONTACT INFORMATION",
        "PROFESSIONAL SUMMARY",
        "SUMMARY",
        "TECHNICAL SKILLS",
        "SKILLS",
        "EXPERIENCE",
        "WORK EXPERIENCE",
        "PROJECTS",
        "EDUCATION",
        "CERTIFICATIONS",
        "ACHIEVEMENTS",
        "LANGUAGES",
        "INTERNSHIPS"
    ]

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.upper() in section_headers:

            story.append(
                Spacer(1, 8)
            )

            story.append(
                Paragraph(
                    line.upper(),
                    section_style
                )
            )

        else:

            if line.startswith("-"):
                line = "• " + line[1:]

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

    doc.build(story)

    return filename