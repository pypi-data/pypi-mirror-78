import streamlit.components.v1 as components
import os

# Create a function _component_func which will call the frontend component when run
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_component_func = components.declare_component(
    "streamlit_custom_tooltip",
    # url="http://localhost:3001",
    path=build_dir,  # Fetch frontend component from local webserver
)

# Define a public function for the package,
# which wraps the caller to the frontend code
def st_custom_tooltip(label: str, textSize: int, selectedAttributes: list, sentence: str):
    component_value = _component_func(label=label, textSize=textSize, selectedAttributes=selectedAttributes, sentence=sentence)
    return component_value
