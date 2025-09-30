import streamlit as st
import openai
import os
# We don't need pandas or dotenv here since the key and data context are passed from the module files.


# Function from the original customquery.py
# MODIFIED: Accepts the openai_key as an argument for secure operation.
def query_chatgpt(question, context, openai_key):
    """
    Queries ChatGPT with a specific question and dataset context.
    The OpenAI key must be passed to this function.
    """
    if not openai_key:
        return "Error: OpenAI API Key is not set."
        
    # Temporarily set the API key for the OpenAI call scope
    # Note: In performance.py, the key is already set globally, but passing it 
    # ensures this function is independent and safer.
    openai.api_key = openai_key 

    prompt = f"""
    Given the following dataset:
    {context}

    Answer the following question consisely and write your final calculation:
    {question}
    """

    prompt2="""You are a teacher who excels in statistics 
    after recieving the data you have to do calculations and answer the query 
    asked by the user you are the best in analyzing data in whole world
    You do not have to show how you are calculating the answers"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role':"system","content":prompt2},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while querying OpenAI: {e}"


# Function from the original animations.py
def display_cards(title, average, highest, lowest):
    """Displays three animated Streamlit cards for average, highest, and lowest metrics."""
    # Create a container for the layout
    with st.container():
        st.subheader(title)
        # Create columns for the layout
        col1, col2, col3 = st.columns(3)

        # Create cards with Streamlit's built-in components
        with col1:
            st.markdown(
                f"""
                <div class="card">
                    <h3 style="font-size: 18px;">Average</h3>
                    <p>{average:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="card">
                    <h3 style="font-size: 18px;">Highest</h3>
                    <p>{highest:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="card">
                    <h3 style="font-size: 18px;">Lowest</h3>
                    <p>{lowest:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Add CSS styles with animations
    st.markdown(
        """
        <style>
        .card {
            background-color: #fff;
            box-shadow: 0 0 1.15px rgba(0, 0, 0, 0.8);
            border-radius: 10px;
            padding: 2px;
            text-align: center;
            font-size: 20px;
            transition: all 0.1s ease;
            -webkit-transition: all 0.5s ease; /* For Safari */
            -moz-transition: all 0.5s ease; /* For Firefox */
        }
        
        .card:hover {
            background-color: #5F6A6A; /* Peach color */
            box-shadow: 0 0 2px rgba(0, 0, 0, 0.8);
            transform: scale(1.1);
            -webkit-transform: scale(1.1); /* For Safari */
            -moz-transform: scale(1.1); /* For Firefox */
            color: #ECF0F1; /* Navy blue color */
        }
        
        .card:hover h3 {
            color: #ECF0F1; /* Navy blue color */
        }
        
        .card h3 {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 3px;
        }
        
        .card p {
            font-size: 15px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )