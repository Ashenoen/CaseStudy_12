from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType

# Set up OpenAI API key
api_key = "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"

# Define the ball specifications
ball_specifications = [
    {"model": "Ball A", "pin_to_buffer": 2.5, "differential": 0.050, "surface_type": "polished", "core_symmetry": "asymmetrical"},
    {"model": "Ball B", "pin_to_buffer": 3.0, "differential": 0.045, "surface_type": "sanded", "core_symmetry": "symmetrical"},
    # Add other balls
]

# Define the player's style (e.g., rev rate, speed)
player_style = {
    "rev_rate": 350,  # In revolutions per minute
    "ball_speed": 18,  # In miles per hour
    "style": "high rev",
}

# Define the oil pattern for the tournament
oil_pattern = {
    "oil_length": 41,  # In feet
    "oil_density": "medium",  # Can be light, medium, or heavy
}

# Define a prompt template for the LangChain agent
prompt_template = """
You are a bowling ball recommendation agent. The player is participating in a tournament with the following oil pattern:
- Oil length: {oil_length} feet
- Oil density: {oil_density}

The player's current arsenal consists of the following balls:
{balls}

The player's style is: {style}

Using this information, build a 6-ball arsenal that will perform well on the given oil pattern. Suggest any additional balls that the player should acquire.
"""

# Create the prompt and LLM chain
template = PromptTemplate(input_variables=["oil_length", "oil_density", "balls", "style"], template=prompt_template)
llm = OpenAI(api_key=api_key, temperature=0.7)
llm_chain = LLMChain(llm=llm, prompt=template)

# Define the tool to fetch bowling ball recommendations
def get_ball_recommendations(oil_length, oil_density, balls, style):
    # Use the LLM chain to process the inputs and generate recommendations
    response = llm_chain.run(oil_length=oil_length, oil_density=oil_density, balls=balls, style=style)
    return response

# Example of usage
recommended_arena = get_ball_recommendations(oil_length=oil_pattern['oil_length'],
                                            oil_density=oil_pattern['oil_density'],
                                            balls=ball_specifications,
                                            style=player_style)
print(recommended_arena)
