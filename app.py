import streamlit as st


from src.modules.performance import performance 
from src.modules.mcq_generator import mcq_generator
from src.modules.lesson_plan import lessonplan
from src.modules.summarizer import summarize
from src.modules.counselor import counselor 

# Set up page configuration
st.set_page_config(page_title="AI Assistant For Teachers", page_icon=":teacher:", layout="centered")

st.markdown("<h1 style='text-align:center;font-family:Garamond,serif;color:#17252A;'>AI Assistant For Teachers</h1>", unsafe_allow_html=True)

st.write("""
<style>
    /* Primary color */
   .stApp {
        background-color: #D3D9D4; /* Light gray background */
    }
    
   .stButton:hover,.stDropdown:hover {
         /* Darker greenish-blue on hover */
    }
    
   /* Accent color */
  .stAlert {
        background-color: #F5B7B1; /* Yellow-orange alert color */
        color: #E74C3C; /* Reddish-orange font color */
    }
    
    /* Text colors */
   .stText {
        color: #212F3C; /* Dark gray text color */
    }
    
   .stHeader {
        color: #212F3C; /* Medium gray header color */
    }
    
   .stMarkdown {
        color: #444; /* Darker gray markdown color */
    }
         
   .stSidebar {
        background-color: #124E66;
    }   
           
   .stInfo {
        background-color: #F5B7B1;
    }
</style>
""", unsafe_allow_html=True)

options = st.sidebar.selectbox("What would you like to do?",["Perform Analysis","Generate Quiz","Generate Lesson Plan","Summarize Lesson","Get Counselling By AI"])

if options == "Perform Analysis":
    performance()

elif options=="Generate Quiz":
    mcq_generator()

elif options=="Generate Lesson Plan":
    lessonplan()

elif options=="Summarize Lesson":
    summarize()

elif options=="Get Counselling By AI":
    # Changed from counsellor() to counselor()
    counselor()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)