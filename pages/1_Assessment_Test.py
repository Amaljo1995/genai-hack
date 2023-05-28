import streamlit as _st
# from utils.Utils import get_choices_from_prompt
from streamlit_chat import message
from utils.Utils import get_completion_from_messages
import random as r
_st.title("Assessment Test")
if 'parsedResume' in _st.session_state:
#     tabs = ['Syntax','Aptitude Test','Coding Assessment']
#     tab1,tab2,tab3 = _st.tabs(tabs)

#     with tab1:
#         pass
#     with tab2:
#         pass
#     with tab3:
#         textPrompt = f'''
# Generate 10 to 20 different coding questions(not theory) to assess the experience-focused coding skills ```based only on given below job description```\n
# job description : + ```{_st.session_state.description}```
# '''
#         questions = get_choices_from_prompt(textPrompt)[0]["text"].split("\n")
#         for question in questions:
#             _st.write(question)

    if "context" not in _st.session_state:
        _st.session_state.context = [ {'role':'system', 'content':"""
You are Testbot, an automated bot/machine/ designed to take tests for candidates based on the applied job role and job description. \
Details on job role and job description is given in the text delimited by triple backticks
    Job Description:
    ```{_st.session_state.description}```
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
"""} ]

    for i,message_ in enumerate(_st.session_state.context):
        if message_['role']=='system':
            continue
        message(message_['content'],is_user=message_['role']=='user',key = str(i))

    placeholder1 = _st.empty()
    placeholder = _st.empty()
    with _st.form('user',clear_on_submit=True):
        prompt = _st.text_area(" ",placeholder='enter..')
        submit = _st.form_submit_button("Submit")
        if submit:
            if prompt.strip()!="":
                _st.session_state.context.append({'role': 'user', 'content': f"{prompt}"})
                with placeholder1.container():
                    message(_st.session_state.context[-1]['content'], is_user=True)
                response = get_completion_from_messages(_st.session_state.context)
                _st.session_state.context.append({'role': 'assistant', 'content': f"{response}"})
                with placeholder.container():
                    message(_st.session_state.context[-1]['content'], is_user=False)
else:
    _st.error('Submit the form to take the test')
    