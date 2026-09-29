
## Novi - AI Personal Assistant
 What it does

An agentic AI assistant that routes user queries to the appropriate specialist and uses tools to complete tasks.

## UI Screenshots
<img width="706" height="447" alt="image" src="https://github.com/user-attachments/assets/6af85f4b-71dc-482c-8d9a-e3cb54de33e0" />

<img width="706" height="447" alt="image" src="https://github.com/user-attachments/assets/6b9033ee-4353-4fa0-924d-cb7541ab3243" />

<img width="620" height="418" alt="image" src="https://github.com/user-attachments/assets/e18fb0d4-f3df-4d84-994b-96a357c6104d" />


<img width="617" height="442" alt="image" src="https://github.com/user-attachments/assets/fe201c96-0301-4765-babc-fca4e3be90be" />


## Live Demo

[Try the AI Personal Assistant](https://novi-ai-personal-assistant.streamlit.app/)
## Agents

- **General Agent:** Handles general questions.
- **Calculation Specialist:** Handles calculations and unit conversions.
- **Research Specialist:** Handles factual and current information using web search.

## Tools

- `calculator(expression)` — Performs calculations.
- `unit_converter(value, from_unit, to_unit)` — Converts units.
- `browser_search` — Searches the web for factual and current information.

## Tech Stack

- Language: Python
- LLM: Groq (`openai/gpt-oss-20b`)
- Function Calling: Groq Tool Use API
- Frontend: Streamlit

## How to Run

### Install dependencies

```bash
pip install -r requirements.txt
````

### Set environment variable

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run

```bash
streamlit run app.py
```

## Sample Interaction

**User:** What is 7 + 1?

→ Handoff → Calculation Specialist
→ Tool: `calculator()`
→ Response: `8`

**User:** Convert 3 kg to pounds.

→ Handoff → Calculation Specialist
→ Tool: `unit_converter()`
→ Response: `6.61 pounds`

**User:** Who is the President of India?

→ Handoff → Research Specialist
→ Tool: `browser_search`
→ Response: Current factual answer

## Project Structure

```text
ai-personal-assistant/
├── main.py
├── app.py
├── agents.py
├── tools.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Environment Variables

| Variable       | Description  |
| -------------- | ------------ |
| `GROQ_API_KEY` | Groq API key |


