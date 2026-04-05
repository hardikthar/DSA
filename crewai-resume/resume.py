import warnings
warnings.filterwarnings('ignore')
    
import fitz  # PyMuPDF for PDF processing
import docx  # python-docx for DOCX processing
import os
from crewai import Agent, Task, Crew

# Preparing Agent and task

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    """Extracts text from a DOCX file using python-docx."""
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return "\n".join(fullText)
    
def extract_text_from_resume(file_path):
    """Determines file type and extracts text."""
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return "Unsupported file format."
    
res1 = extract_text_from_resume('/home/hardik/Hardik thar cv.pdf')
print(res1)

res2 = extract_text_from_resume('/home/hardik/hardik thar CV.docx')
print(res2)
    
with open('/home/hardik/crewai_resume/claude.txt', 'r') as file:
    claude_key = file.read().strip()

os.environ['ANTHROPIC_API_KEY'] = claude_key
os.environ["ANTHROPIC_MODEL_NAME"] = 'claude-sonnet-4-20250514'

# Agent 1: Resume Strategist
resume_feedback = Agent(
    role="Professional Resume Advisor",
    goal="Give feedback on the resume to make it stand out in the job market.",
    verbose=True,
    backstory="With a strategic mind and an eye for detail, you excel at providing feedback on resumes to highlight the most relevant skills and experiences."
    )
# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_feedback_task = Task(
    description=(
        """Give feedback on the resume to make it stand out for recruiters.
        Review every section, inlcuding the summary, work experience, skills, and education. Suggest to add relevant sections if they are missing.
        Also give an overall score to the resume out of 10.  This is the resume: {resume}"""
    ),
    expected_output="The overall score of the resume followed by the feedback in bullet points.",
    agent=resume_feedback
)
# Agent 2: Resume Strategist
resume_advisor = Agent(
    role="Professional Resume Writer",
    goal="Based on the feedback recieved from Resume Advisor, make changes to the resume to make it stand out in the job market.",
    verbose=True,
    backstory="With a strategic mind and an eye for detail, you excel at refining resumes based on the feedback to highlight the most relevant skills and experiences."
)
# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_advisor_task = Task(
    description=(
        """Rewrite the resume based on the feedback to make it stand out for recruiters. You can adjust and enhance the resume but don't make up facts.
        Review and update every section, including the summary, work experience, skills, and education to better reflect the candidates abilities. This is the resume: {resume}"""
    ),
    expected_output= "Resume in markdown format that effectively highlights the candidate's qualifications and experiences",
    # output_file="improved_resume.md",
    context=[resume_feedback_task],
    agent=resume_advisor
)

from crewai_tools import SerperDevTool
with open('/home/hardik/crewai_resume/serper.txt', 'r') as file:
    serper_key = file.read()

os.environ["SERPER_API_KEY"] = serper_key

search_tool = SerperDevTool()

# Agent 3: Researcher
job_researcher = Agent(
    role = "Senior Recruitment Consultant",
    goal = "Find the 5 most relevant, recently posted jobs based on the improved resume recieved from resume advisor and the location preference",
    tools = [search_tool],
    verbose = True,
    backstory = """As a senior recruitment consultant your prowess in finding the most relevant jobs based on the resume and location preference is unmatched.
    You can scan the resume efficiently, identify the most suitable job roles and search for the best suited recently posted open job positions at the preffered location."""
    )

research_task = Task(
    description = """Find the 5 most relevant recent job postings based on the resume recieved from resume advisor and location preference. This is the preferred location: {location} .
    Use the tools to gather relevant content and shortlist the 5 most relevant, recent, job openings""",
    expected_output=(
        "A bullet point list of the 5 job openings, with the appropriate links and detailed description about each job, in markdown format"
    ),
#    output_file="relevant_jobs.md",
    agent=job_researcher
)

#create crew ai
crew = Crew(
    agents=[resume_feedback, resume_advisor, job_researcher],
    tasks=[resume_feedback_task, resume_advisor_task, research_task],
    verbose=True
)

result = crew.kickoff(inputs={"resume": res2, "location": 'Dallas'})

from IPython.display import Markdown, display

markdown_content = resume_feedback_task.output.raw.strip("```markdown").strip("```").strip()
# Display the Markdown content
display(Markdown(markdown_content))

markdown_content = resume_advisor_task.output.raw.strip("```markdown").strip("```").strip()
# Display the Markdown content
display(Markdown(markdown_content))

markdown_content = research_task.output.raw.strip("```markdown").strip("```").strip()
# Display the Markdown content
display(Markdown(markdown_content))
