import openai
import PyPDF2
import docx
from pyresparser import ResumeParser
import streamlit as _st
import panel as pn

with open("./utils/OpenAIkey.txt","r") as key:
    openai.api_key = key.read().strip()

def extract_information(file_path):
    data = ResumeParser(file_path).get_extracted_data()
    mobile_number = data['mobile_number'] if data['mobile_number'] and len(data['mobile_number']) >= 10 else ""
    extracted_data = {
        'Name': data.get('name', ''),
        'Email': data.get('email', ''),
        'Phone': mobile_number,
        'Experience(yrs)': data.get('total_experience', ''),
        'Experience': data.get("experience", ''),
        "Company_Names": data.get("company_names", []),
        'Skills': ', '.join(data.get('skills', [])),
        'Degree': data.get('degree', '')
    }
    return extracted_data
@_st.cache_data
def get_choices_from_prompt(text_prompt):
    response = openai.Completion.create(
        prompt=text_prompt,
        temperature=0,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003"
    )

    choices = response.choices
    return choices

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

@_st.cache_data
def analyze_resume(resume_text,job_description):
    prompt=f"""
    You're an excellent talent advisor who can analyze the candidate's resume in relation to job description. Identify the key skills, experiences, and qualifications that the candidate possesses and those that are required for the and targeted job description. Information about the candidate's resume, and job description are given inside text delimited by triple backticks.Summarize the analysis using <at most> 500 tokens brief & concised. 
    Candidate's Resume :
    ```{resume_text}```

    Job Description for the Target Role:
    ```{job_description}```
    """
    resume_analysis = get_completion(prompt)
    return resume_analysis

def convert_files_to_text(file_path):
    if file_path.endswith('.pdf'):
        text = convert_pdf_to_text(file_path)
    elif file_path.endswith('.docx'):
        text = convert_docx_to_text(file_path)
    else:
        return ""
    
    return text

def convert_pdf_to_text(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def convert_docx_to_text(file_path):
    doc = docx.Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def assessment_test(job_description):
    def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    
        return response.choices[0].message["content"]
    
    def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,  # this is the degree of randomness of the model's output
        )
        return response.choices[0].message["content"]

    def collect_messages(_):
        prompt = inp.value_input
        inp.value = ''
        context.append({'role': 'user', 'content': f"{prompt}"})
        response = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': f"{response}"})
        panels.append(
            pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
        panels.append(
            pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
        return pn.Column(*panels)

    pn.extension()

    panels = []  # collect display
    context = [ {'role':'system', 'content':"""
You are Testbot, an automated bot/machine/ designed to take tests for candidates based on the applied job role and job description. \
Details on job role and job description is given in the text delimited by triple backticks
    Job Description:
    ```{job_description}```
    It's a must to follow the follwing steps:
    Determine the relevant topics: Based on the job description , identify the key topics for the job role. These topics may include data structures, algorithms, databases, system design, machine learning, etc./
    Select appropriate questions: Create a pool of questions for each topic, covering different difficulty levels. The questions can be sourced from existing training data with which you are trained; they can be from any website or created specifically for this assessment test./
    Determine the number of questions: Based on the importance and relevance of each topic, decide the number of questions to be included in the assessment test. You can assign weights to different topics and allocate a proportional number of questions based on their importance./
    Randomly select questions: randomly select questions from the question pool for each topic to form the assessment test. Ensure that the difficulty levels are appropriately distributed./    

You first greet the candidate, then start asking the questions one by one, \.
So it should have 1. Three Coding Test  2. Seven job role specific multiple choices .It should be in format of other coding preparation platforms
You collect the answer response for entire questionnare, then evaluate based on the evaluation criteria given below \
Designing a scoring or grading system for a coding preparation platform requires a detailed understanding of the learning objectives and the skills you're testing. Here's a general approach that you might consider:

1. Problem Complexity

You could grade problems based on their complexity. Basic problems, such as those related to syntax or fundamental concepts, could be scored lower, while more complex problems, such as those involving algorithms and data structures, could have a higher score.

Easy: 1-10 points
Medium: 11-20 points
Hard: 21-30 points
2. Code Quality

An AI-powered code review system could be used to evaluate the quality of the code submitted. This could look at factors like:

Correctness: Is the solution correct and does it solve the problem as intended?
Efficiency: How optimal is the code in terms of time and space complexity?
Readability: Is the code easy to read and understand?
Conformity to standards: Does the code adhere to coding standards and best practices?. \

For MCQ get the answer A,B,C,D and verify the answer yourself.\
"""} ]  # accumulate messages
   

    inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
    button_conversation = pn.widgets.Button(name="Chat!")

    interactive_conversation = pn.bind(collect_messages, button_conversation)

    dashboard = pn.Column(
        inp,
        pn.Row(button_conversation),
        pn.panel(interactive_conversation, loading_indicator=True, height=300),
    )

    pn.serve(dashboard)

    # After the conversation is over, create a JSON file
    '''messages =  context.copy()
    messages.append(
    {'role':'system', 'content':'create a json summary of the previous question and answers. Itemize the evaluation for each question and answer\
     The fields should be 1) question  2) answer 3) candidate response  4)evaluation qualified and quantified '},    
    )   

    response = get_completion_from_messages(messages, temperature=0)
    print(response)'''
