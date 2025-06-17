from .openai_client import ask_openai

def agent_1(promt: str) -> str:
    return ask_openai(f"You are allknown bot, answer shortly on question: {promt}")

def agent_2(reply: str) -> str:
    return ask_openai(f"You are analyzer. Check and make the answer better: {reply}")

def run_a2a(promt: str) -> str:
    interm = agent_1(promt)
    final = agent_2(interm)
    return final