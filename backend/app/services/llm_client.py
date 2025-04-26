from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from app.config import settings

@tool
def get_weather(location: str) -> str:
    """Gets the current weather."""
    # In a real scenario, this would call a weather API
    # For this example, it just returns a fixed string
    return "Touch some grass."

class LLMClient:
    def __init__(self):
        llm = ChatOpenAI(
            api_key=settings.llm_api_key,
            temperature=settings.temperature,
            model_name=settings.model_name,
            max_tokens=settings.max_tokens
        )
        
        tools = [get_weather]
        
        # Define the prompt template
        # Note: Adjust the prompt if using a different model or structure
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant."),
                ("human", "{input}"),
                ("ai", "{agent_scratchpad}"), # Placeholder for agent's intermediate steps
            ]
        )

        # Create the agent
        agent = create_openai_tools_agent(llm, tools, prompt)

        # Create the agent executor
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # Added verbose=True for debugging

    def get_response(self, question: str) -> str:
        """Get a response from the LLM agent."""
        try:
            # Use the agent executor to handle the question, potentially using tools
            response = self.agent_executor.invoke({"input": question})
            return response.get("output", "No output found") # Agent response structure might vary
        except Exception as e:
            # Log the error here if needed
            raise Exception(f"Failed to get response from LLM agent: {str(e)}")

def get_llm_client() -> LLMClient:
    """Factory function to get an LLM client instance."""
    return LLMClient() 