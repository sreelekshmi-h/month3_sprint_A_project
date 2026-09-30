import os
import json
from groq import Groq,RateLimitError
from dotenv import load_dotenv
import re

from tools import calculator, unit_converter

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-20b"


# -----------------------------
# TOOL SCHEMAS
# -----------------------------

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Calculate a mathematical expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression such as 25 * 48"
                }
            },
            "required": ["expression"]
        }
    }
}


unit_converter_tool = {
    "type": "function",
    "function": {
        "name": "unit_converter",
        "description": "Convert a value from one supported unit to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "The value to convert"
                },
                "from_unit": {
                    "type": "string",
                    "description": "Original unit"
                },
                "to_unit": {
                    "type": "string",
                    "description": "Target unit"
                }
            },
            "required": ["value", "from_unit", "to_unit"]
        }
    }
}


web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for factual or current information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
}


# -----------------------------
# CALCULATION SPECIALIST
# -----------------------------

def calculation_specialist(user_query, conversation_history):

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in conversation_history
        if message.get("content") and not message.get("error")
    ]

    messages = [
        {
            "role": "system",
            "content": """
You are the Calculation Specialist.

You handle calculations and unit conversions.

Use the provided tools to perform calculations or conversions.

After receiving a tool result, give only the final answer.
Do not call another tool after receiving a tool result.
Do not output Python code or internal instructions.
"""
        }
    ]

    messages.extend(history)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[
            calculator_tool,
            unit_converter_tool
        ]
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    tool_call = message.tool_calls[0]

    if tool_call.function.name == "calculator":
        args = json.loads(tool_call.function.arguments)
        result = calculator(args["expression"])

    elif tool_call.function.name == "unit_converter":
        args = json.loads(tool_call.function.arguments)

        result = unit_converter(
            args["value"],
            args["from_unit"],
            args["to_unit"]
        )

    else:
        return "Unable to process the calculation."

    messages.append(message)

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result
    })

    try:
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tool_choice="none"
        )

        return final_response.choices[0].message.content

    except Exception as e:
        print("\n[ERROR]")
        print("The calculation could not be completed.")
        print(f"Error details: {e}")

        return "Sorry, I couldn't complete that calculation."

# -----------------------------
# RESEARCH SPECIALIST
# -----------------------------
def research_specialist(user_query, conversation_history):

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in conversation_history
        if message.get("content") and not message.get("error")
    ]

    messages = [
        {
            "role": "system",
            "content": """
You are the Research Specialist.

You handle factual and current information requests.

Use browser search when the user needs:

- current information
- recent information
- factual information that should be verified

Use the conversation history when relevant.

Give a clear and concise final answer.

Do not mention internal agent routing.
Do not output Python code or internal instructions.
"""
        }
    ]

    messages.extend(history)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[
                {
                    "type": "browser_search"
                }
            ],
            tool_choice="required"
        )

        return response.choices[0].message.content

    except RateLimitError:
        print("\n[ERROR]")
        print("Groq API rate limit reached.")

        return "Sorry, the AI service has reached its usage limit. Please try again later."

    except Exception as e:
        print("\n[ERROR]")
        print(f"Error details: {e}")

        return "Sorry, I couldn't complete the research request."
# -----------------------------
# GENERAL AGENT
# -----------------------------

def general_agent(user_query, conversation_history):

    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in conversation_history
        if message.get("content") and not message.get("error")
    ]

    messages = [
        {
            "role": "system",
            "content": """
You are the General Agent of an AI Personal Assistant.

You answer normal conversational questions.

Calculation, unit conversion, and research requests are
already routed by the application.

Use the conversation history to understand previous messages.

Do not mention internal agent routing.
Do not output Python code or internal instructions.

Answer clearly and concisely.
"""
        }
    ]

    messages.extend(history)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        return response.choices[0].message.content

    except RateLimitError:
        print("\n[ERROR]")
        print("Groq API rate limit reached.")

        return "Sorry, the AI service has reached its usage limit. Please try again later."

    except Exception as e:
        print("\n[ERROR]")
        print(f"Error details: {e}")

        return "Sorry, I couldn't process your request."

def route_query(user_query):
    query = user_query.lower().strip()

    calculation_words = [
        "calculate",
        "convert",
        "plus",
        "minus",
        "multiply",
        "divide",
        "kg",
        "kilogram",
        "pound",
        "pounds",
        "km",
        "kilometer",
        "mile",
        "miles",
        "feet",
        "meter",
        "meters"
    ]

    research_words = [
        "latest",
        "current",
        "today",
        "weather",
        "temperature",
        "president",
        "prime minister",
        "who is",
        "where is",
        "when did",
        "news",
        "trained",
        "training"
    ]

    # Arithmetic operators + numbers
    if re.search(r"\d+\s*[+\-*/%]\s*\d+", query):
        return "CALCULATION"

    if any(word in query for word in calculation_words):
        return "CALCULATION"

    if any(word in query for word in research_words):
        return "RESEARCH"

    return "DIRECT"



# -----------------------------
# MAIN HANDOFF FUNCTION
# -----------------------------

def handle_query(user_query, conversation_history):

    decision = route_query(user_query)

    if decision == "CALCULATION":
        print("\n[HANDOFF]")
        print("From: General Agent")
        print("To: Calculation Specialist")
        print("Reason: User requested calculation or unit conversion")
        print(f"Context: {user_query}")
        print("[/HANDOFF]\n")

        return calculation_specialist(
            user_query,
            conversation_history
        )

    elif decision == "RESEARCH":
        print("\n[HANDOFF]")
        print("From: General Agent")
        print("To: Research Specialist")
        print("Reason: User requested factual or current information")
        print(f"Context: {user_query}")
        print("[/HANDOFF]\n")

        return research_specialist(
            user_query,
            conversation_history
        )

    else:
        return general_agent(
            user_query,
            conversation_history
        )
