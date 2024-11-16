import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import json

# Set up OpenAI API key
api_key = "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"

# Define the LangChain model
llm = OpenAI(api_key=api_key, temperature=0.7)

# Define the prompt template for generating ball recommendations
prompt_template = """
You are a bowling ball recommendation agent. The player is participating in a tournament with the following oil pattern:
- Oil length: {oil_length} feet
- Oil density: {oil_density}

The player's current arsenal consists of the following balls:
{balls}

The player's style is: {style}

Using this information, build a 6-ball arsenal that will perform well on the given oil pattern. Suggest any additional balls that the player should acquire.
"""


# Streamlit App Interface
def get_ball_recommendations(oil_length, oil_density, balls, style):
    template = PromptTemplate(input_variables=["oil_length", "oil_density", "balls", "style"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=template)
    response = llm_chain.run(oil_length=oil_length, oil_density=oil_density, balls=balls, style=style)
    return response


# Streamlit UI
st.title("Bowling Ball Arsenal Builder")
st.header("Create Your Perfect 6-Ball Arsenal")

# User Input Section for Balls the Player Currently Owns
st.subheader("Enter Your Current Bowling Balls")
ball_1 = st.text_input("Ball 1 - Model (e.g., 'Ball A')", "")
ball_1_pin_buffer = st.number_input("Pin-to-buffer distance for Ball 1", min_value=0.0, max_value=10.0, value=2.5)
ball_1_differential = st.number_input("Differential for Ball 1", min_value=0.0, max_value=0.1, value=0.050)
ball_1_surface = st.selectbox("Surface type for Ball 1", ["Polished", "Sanded", "Matte"])
ball_1_core = st.selectbox("Core type for Ball 1", ["Symmetrical", "Asymmetrical"])

# Add more balls similarly
ball_2 = st.text_input("Ball 2 - Model", "")
ball_2_pin_buffer = st.number_input("Pin-to-buffer distance for Ball 2", min_value=0.0, max_value=10.0, value=3.0)
ball_2_differential = st.number_input("Differential for Ball 2", min_value=0.0, max_value=0.1, value=0.045)
ball_2_surface = st.selectbox("Surface type for Ball 2", ["Polished", "Sanded", "Matte"])
ball_2_core = st.selectbox("Core type for Ball 2", ["Symmetrical", "Asymmetrical"])

# User Input Section for Player's Style
st.subheader("Enter Your Bowling Style")
rev_rate = st.number_input("Rev Rate (in RPM)", min_value=100, max_value=800, value=350)
ball_speed = st.number_input("Ball Speed (in MPH)", min_value=10, max_value=30, value=18)
style = st.selectbox("Bowling Style", ["High Rev", "Medium Rev", "Low Rev"])

# User Input Section for Oil Pattern
st.subheader("Enter Tournament Oil Pattern")
oil_length = st.number_input("Oil Length (in feet)", min_value=30, max_value=50, value=41)
oil_density = st.selectbox("Oil Density", ["Light", "Medium", "Heavy"])

# Collect all user input into a dictionary
current_balls = [
    {
        "model": ball_1,
        "pin_to_buffer": ball_1_pin_buffer,
        "differential": ball_1_differential,
        "surface_type": ball_1_surface,
        "core_symmetry": ball_1_core
    },
    {
        "model": ball_2,
        "pin_to_buffer": ball_2_pin_buffer,
        "differential": ball_2_differential,
        "surface_type": ball_2_surface,
        "core_symmetry": ball_2_core
    },
    # Add other balls similarly
]

# Convert the list of balls into a string format for the LangChain agent
balls_json = json.dumps(current_balls, indent=4)

# Show the final button to get recommendations
if st.button("Get My 6-Ball Arsenal"):
    with st.spinner('Generating recommendations...'):
        # Get ball recommendations from the agent
        recommended_arena = get_ball_recommendations(
            oil_length=oil_length,
            oil_density=oil_density,
            balls=balls_json,
            style=style
        )

        st.subheader("Recommended 6-Ball Arsenal")
        st.write(recommended_arena)
