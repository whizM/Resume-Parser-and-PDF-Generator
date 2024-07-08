import streamlit as st
import re
import tempfile
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
    return text

def extract_name(text):
    match = re.search(r'^[^\n]+', text)
    return match.group() if match else ""

def extract_skills(text):
    pattern = re.compile(r'(?:Skills|Technologies|Tools):?\s*(.*?)(?:Experience|Education|Projects|Hackathons|Achievements|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_experience(text):
    pattern = re.compile(r'Experience:?\s*(.*?)(?:Education|Projects|Hackathons|Achievements|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_education(text):
    pattern = re.compile(r'Education:?\s*(.*?)(?:Projects|Hackathons|Achievements|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_projects(text):
    pattern = re.compile(r'Projects:?\s*(.*?)(?:Hackathons|Achievements|Skills|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_hackathons(text):
    pattern = re.compile(r'Hackathons:?\s*(.*?)(?:Achievements|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def extract_achievements(text):
    pattern = re.compile(r'Achievements:?\s*(.*?)(?:Education|Projects|Hackathons|Work|Languages|$)', re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""

def create_resume_pdf(name, skills, experience, achievements, education, hackathons, projects, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Professional Resume", styles['Title']))
    content.append(Spacer(1, 12))

    if name:
        content.append(Paragraph("Name:", styles['Heading2']))
        content.append(Paragraph(name, styles['Normal']))
        content.append(Spacer(1, 12))

    if skills:
        content.append(Paragraph("Skills:", styles['Heading2']))
        content.append(Paragraph(skills, styles['Normal']))
        content.append(Spacer(1, 12))

    if experience:
        content.append(Paragraph("Experience:", styles['Heading2']))
        content.append(Paragraph(experience, styles['Normal']))
        content.append(Spacer(1, 12))

    if achievements:
        content.append(Paragraph("Achievements:", styles['Heading2']))
        content.append(Paragraph(achievements, styles['Normal']))
        content.append(Spacer(1, 12))

    if education:
        content.append(Paragraph("Education:", styles['Heading2']))
        content.append(Paragraph(education, styles['Normal']))
        content.append(Spacer(1, 12))

    if hackathons:
        content.append(Paragraph("Hackathons:", styles['Heading2']))
        content.append(Paragraph(hackathons, styles['Normal']))
        content.append(Spacer(1, 12))

    if projects:
        content.append(Paragraph("Projects:", styles['Heading2']))
        content.append(Paragraph(projects, styles['Normal']))
        content.append(Spacer(1, 12))

    doc.build(content)

# Streamlit frontend
st.title("Resume Parser and PDF Generator")

uploaded_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")

if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    if resume_text:
        name = extract_name(resume_text)
        skills = extract_skills(resume_text)
        experience = extract_experience(resume_text)
        education = extract_education(resume_text)
        projects = extract_projects(resume_text)
        hackathons = extract_hackathons(resume_text)
        achievements = extract_achievements(resume_text)

        st.write(" ")
        st.write(f"**Resume of:** {name} ")
        st.write(" ")
        st.write(f"**Name:** {name}")
        st.write(f"**Skills:** {skills}")
        st.write(f"**Experience:** {experience}")
        st.write(f"**Achievements:** {achievements}")
        st.write(f"**Education:** {education}")
        st.write(f"**Hackathons:** {hackathons}")
        st.write(f"**Projects:** {projects}")
        st.write(" ")

        if st.button("Generate PDF"):
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                create_resume_pdf(name, skills, experience, achievements, education, hackathons, projects, tmp_file.name)
                st.write(" ")
                st.write("Click below to download the PDF:")
                st.download_button(
                    label="Download PDF",
                    data=open(tmp_file.name, "rb").read(),
                    file_name=f"Converted_Resume.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("No text could be extracted from the uploaded PDF.")
