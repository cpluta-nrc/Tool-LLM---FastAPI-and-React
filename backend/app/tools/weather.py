from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Gets the current weather."""
    # In a real scenario, this would call a weather API
    # For this example, it just returns a fixed string
    return "Touch some grass." 