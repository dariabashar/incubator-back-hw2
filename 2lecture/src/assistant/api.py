from fastapi import APIRouter, Request
from .a2a import run_a2a

router = APIRouter(prefix="/assistant", tags=["assistant"])

@router.post("/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "No prompt provided"}
    
    response = run_a2a(prompt)
    return {"response": response}