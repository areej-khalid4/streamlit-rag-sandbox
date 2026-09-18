import time
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.callbacks import BaseCallbackHandler

@tool
def run_calc(expression: str) -> str:
    """Calculates mathematical expression values (e.g. '5+5'). Input should be a math string."""
    try:
        clean_expr = "".join(c for c in expression if c in "0123456789+-*/() ")
        return str(eval(clean_expr))
    except Exception as e:
        return f"Error: {e}"

@tool
def run_clock(query: str) -> str:
    """Finds the current system local clock date/time."""
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_agent_tools():
    return [run_calc, run_clock]

def get_react_prompt():
    return PromptTemplate.from_template(
        "Answer the following questions as best you can. You have access to the following tools:\n\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "CRITICAL: You must only write ONE single step at a time (ONE Thought + ONE Action/Action Input OR ONE Final Answer). Do NOT repeat the Question. Do NOT write 'Observation:' yourself. Write your single step and then STOP immediately.\n\n"
        "Begin!\n\n"
        "Question: {input}\n"
        "Thought: {agent_scratchpad}"
    )

class StreamlitTraceCallback(BaseCallbackHandler):
    def __init__(self, log_container, logs_list):
        self.log_container = log_container
        self.logs_list = logs_list

    def on_agent_action(self, action, **kwargs):
        self.logs_list.append(f"🔍 **Thought/Action**: {action.log}")
        self.log_container.markdown("\n\n".join(self.logs_list))

    def on_tool_end(self, output, **kwargs):
        self.logs_list.append(f"📥 **Observation**: {output}")
        self.log_container.markdown("\n\n".join(self.logs_list))
