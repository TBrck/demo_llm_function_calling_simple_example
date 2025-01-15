"""
test_llm_function_calling_simple_example.py

This script is designed to demo and test basic function calling capabilities powered by Large Language Models (LLMs).
"""

# Import necessary modules
import os
import json

from typing import Any, List, Dict

from openai import AzureOpenAI
from openai import BadRequestError

from tools.available_tools import *

# Create the LLM client which will be used to interact with the LLM API
os.environ["AZURE_OPENAI_API_KEY"] = "your_azure_openai_api_key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "your_azure_openai_endpoint"

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-06-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Define the completion function
def get_completion(messages: List[Dict], require_function: bool = True) -> Any:
    # tool_choice = "required" if require_function else None
    try:
        if(require_function==False):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.5
            )
            return response # .choices[0].message
        else:
            print("Calling completion with AVAILABLE_TOOLS")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=AVAILABLE_TOOLS,
                temperature=0.5
            )
            return response # .choices[0].message
    except BadRequestError as bre:
            print(f"An error occurred: {bre}")
            return "Error occurred: BadRequestError"
    except Exception as e:
        # Handle other exceptions
        print(f"An unexpected error occurred: {e}")
        return "Error occurred: Unexpected"
    
# Define the function to call the LLM
def call_llm_function(messages: List[Dict], require_function: bool = True) -> Any:
    # Call the get_completion function
    response = get_completion(messages, require_function)
    return response

# Make sure the LLM gets called when the program is executed from the command line
if __name__ == "__main__":
    user_content = input("Please enter your message: ")
    test_messages = [
        {"role": "system", "content": """
            You are an LLM that selects the best function alongside its parameters from the available tools,
            and asks the user for missing information if necessary.
            If there is a function in the available tools that matches the request, you MUST call the function.
            Only ask for additional information if it's absolutely necessary for the call of the function you selected.
        """},
        {"role": "user", "content": user_content}
    ]
    response = call_llm_function(test_messages, require_function=True)
    response_message = response.choices[0].message
    
    # Ensure the assistant responds with a message if any information is missing for the function calling
    if response_message.content:
        print(response_message.content)
    # Ensure the assistant calls the function, with the correct arguments, if all information is available
    elif response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            arguments = tool_call.function.arguments

            # Convert arguments from JSON string to dictionary
            args_dict = json.loads(arguments)

            # Call the function from available tools
            if function_name in globals():
                function_to_call = globals()[function_name]
                result = function_to_call(**args_dict)
                print(f"Result of {function_name}: {result}")
            else:
                print(f"Function {function_name} not found in available tools.")