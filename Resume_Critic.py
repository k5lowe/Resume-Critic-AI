from pypdf import PdfReader
import spacy
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re




criteria = {
    'pages': 10,
    'spelling': 2,
    'capital': 2,
    'verbs': 3,
    'chronological': 5,
    'github': 10,
    'linkedin': 5,
    'run on sentence': 3,
    'objective': 5,
    'tense': 2,
    'resume match descrip': 5,
    'keywords': 1
}


load_dotenv(r"C:\Users\kushi\OneDrive\Documents\Python Projects\Resume_Critic\.env")
gemini_api_key = os.getenv('API_KEY')                    # REPLACE API_KEY WITH THE NAME OF THE API KEY IN YOUR .env FILE (NOT THE VALUE)


try:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    print(f"An error occurred:\n {e}")


RESUME_SCORE = 100
RESUME_FEEBACK = ""



# path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (Jan 14).pdf"
# path = r"C:\Users\kushi\OneDrive\Documents\University\11. Winter 2025\Coop\Kushini Lowe - Resume (TEST).pdf"
path = r"C:\Users\kushi\Downloads\software-engineer-resume-example.pdf"         #REPLACE THIS WITH YOUR OWN RESUME/DUMMY RESUME
reader = PdfReader(path)
page = reader.pages[0]
text = page.extract_text()



# 1. Length of Resume
def resume_length(resume):
    if len(reader.pages) > 1:
        score = criteria['pages']
        resume_feedback = "Resume is longer than one page"
    else:
        resume_feedback = ""
        score = 0
    return resume_feedback, score



# 2. Spelling
def spelling_errors(resume):
    prompt = f"""Identify all spelling errors in this text {resume}. Check for mistakes in city names 
    and within each section, including Skills, Education, Experience, Projects, Certifications, etc.
    The output should ONLY be a list of spelling errors. 
    For ex ["'incorect' should be 'incorrect'", "'wods' should be 'words'"]"""

    response = model.generate_content(prompt)
    response_text = response.text
    score = (response_text.lower()).count(' should ')
    # print("amount of spelling errors: ", score)

    return response_text, score



# 3. Github
def git_hub(resume):
    prompt = f"""Check if a GitHub profile link is present in the provided text: {resume}.  
    If a GitHub profile is found, return **1**.  
    If no GitHub profile is found, return **0**.  
    Only return **1 or 0**, without any additional text or explanation."""

    response = model.generate_content(prompt)
    response_text = response.text

    if '0' in response_text:
        reason = "Github profile not provided"
        score = criteria['github']
    else:
        reason = ""
        score = 0

    return reason, score



# 4. Linkedin
def linkedin(resume):
    prompt = f"""Check if a Linkedin profile link is present in the provided text: {resume}.  
    If a Linkedin profile is found, return **1**.  
    If no Linkedin profile is found, return **0**.  
    Only return **1 or 0**, without any additional text or explanation."""

    response = model.generate_content(prompt)
    response_text = response.text

    if '0' in response_text:
        reason = "Linkedin profile not provided"
        score = criteria['linkedin']
    else:
        reason = ""
        score = 0

    return reason, score



# 5. Objective
def objective(resume):
    prompt = f"""Check if resume: {resume} has an objective section.  
    If an objective section is found, return **1**.  
    If no objective section is found, return **0**.  
    Only return **1 or 0**, without any additional text or explanation."""

    response = model.generate_content(prompt)
    response_text = response.text

    if '1' in response_text:
        reason = "An Objective section has been detected"
        score = criteria['objective']
    else:
        reason = ""
        score = 0

    return reason, score



# 6. Keywords
def keywords(resume,keys):
    missing_keywords = []
    resume = resume.lower()
    score = 0
    for key in keys:
        if key.lower() not in resume:
            score += criteria['keywords']
            missing_keywords.append(key)
        else:
            score += 0
    
    return missing_keywords, score



def user_input_job_description():
    job_description = input("Please enter a job description: \n")

    prompt = f"""Format the following job description {job_description} in a clean, professional, and 
    well-structured manner. Ensure proper use of headings, bullet points, and spacing 
    for readability. Maintain clarity while preserving all key details.
    """
    response = model.generate_content(prompt)
    return response.text
    
    

def keywords_wrapper(job_description):
    prompt = f"""Extract the most relevant keywords from the following job description:  

    {job_description}  

    The keywords should include:  
    - **Technical skills** (e.g., programming languages, tools, frameworks)  
    - **Soft skills** (e.g., communication, leadership)  
    - **Job-related terms** (e.g., responsibilities, qualifications)  
    - **Industry-specific terms** (e.g., methodologies, certifications)  

    Return only a **comma-separated list of keywords**, without any additional text or explanations."""

    response = model.generate_content(prompt)
    return response.text.split(',')



def main_function(resume):
    JD = user_input_job_description()
    RL = resume_length(text)
    SE = spelling_errors(text)
    GH = git_hub(text)
    LN = linkedin(text)
    OB = objective(text)
    KY = keywords(text,keywords_wrapper(JD))
    
    RESUME_SCORE = 100 - (RL[1] + SE[1] + GH[1] + LN[1] + OB[1] + KY[1])
    RESUME_FEEDBACK = f"{RL[0]}\n{SE[0]}\n{GH[0]}\n{LN[0]}\n{OB[0]}\n You are missing these keywords: \n {KY[0]}"

    print(RESUME_FEEDBACK)
    print()
    print(RESUME_SCORE)



if __name__ == '__main__':
    main_function(text)