from pypdf import PdfReader
import spacy
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.configure(api_key=api_key)

# path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (Jan 14).pdf"
path = r"C:\Users\kushi\Downloads\software-engineer-resume-example.pdf"
reader = PdfReader(path)
page = reader.pages[0]
text = page.extract_text()


def resume_sections(resume):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Find the names of sections in the resume given: {resume}. \
        For example: Skills,Education,Experience,Projects,Certifications"
    response = model.generate_content(prompt)
    return response.text

# Test the API
prompt = "Find the names of sections in the resume given"
response = resume_sections(text)
print(response)