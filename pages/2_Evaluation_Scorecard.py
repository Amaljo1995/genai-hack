import streamlit as _st
from utils.Utils import analyze_resume,convert_files_to_text
styles='''
<style>
p{
text-align:justify;
}
</style>
'''
_st.markdown(styles,True)
_st.title('Evaluation Scorecard')

if 'file' in _st.session_state:
    col1,col2 = _st.columns(2)
    col1.subheader('Resume Evaluation')
    col2.subheader('Assessment Test Evalutaion')
    resumeText = convert_files_to_text(_st.session_state.file)
    col1.write(analyze_resume(resumeText,_st.session_state.description))
    col2.write("Sudheendra Rao, the first candidate, performed exceptionally well in the coding test for the Python developer role. He showcased strong development skills, excellent efficiency, and a solid understanding of Python syntax and best practices. Sajiths code demonstrated clear thinking, logical organization, and adherence to proper coding conventions. Additionally, he exhibited a deep understanding of time complexity and implemented efficient algorithms.Sajiths solution was not only correct but also optimized for performance. He effectively utilized data structures and algorithms to solve the problem, resulting in an efficient implementation. His code was well-documented, making it easy to understand and maintain. Overall, Sajiths performance reflects his experience and proficiency as a Python developer")