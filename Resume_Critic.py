from pypdf import PdfReader
import spacy
import google.generativeai as genai
from dotenv import load_dotenv
import os


load_dotenv(r"C:\Users\kushi\OneDrive\Documents\Python Projects\Resume_Critic\.env")
gemini_api_key = os.getenv('API_KEY')                    # REPLACE API_KEY WITH THE NAME OF THE API KEY IN YOUR .env FILE (NOT THE VALUE)


try:

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    # response = model.generate_content("Write me a poem about the a white bunny")
    # print(response.text)

except Exception as e:
    print(f"An error occurred:\n {e}")


RESUME_SCORE = 100
RESUME_FEEDBACK = []


# path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (Jan 14).pdf"
# path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (TEST).pdf"
path = r"C:\Users\kushi\Downloads\software-engineer-resume-example.pdf"         #REPLACE THIS WITH YOUR OWN RESUME/DUMMY RESUME
reader = PdfReader(path)
page = reader.pages[0]
text = page.extract_text()

# print(text)

# 1st Criteria
if len(reader.pages) > 1:
    RESUME_SCORE -= 10
    RESUME_FEEDBACK.append("Resume is longer than one page")





def spelling_errors(resume):
    prompt = f'''Identify all spelling errors in this text {resume}. Check for mistakes in city names and within
          each section, including Skills, Education, Experience, Projects, and Certifications.
          Provide the misspelled words along with suggestions for correction.'''

    response = model.generate_content(prompt)
    return response.text



response = spelling_errors(text)
print(response)
print(len(response))