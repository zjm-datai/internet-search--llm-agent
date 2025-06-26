import asyncio 
import random
import janus

from typing import Union, List, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field

from core.agent import init_agent 

def parse_arguments():
    import argparse 

    parser = argparse.ArgumentParser(description="MySearch API")
    parser.add_argument("--host", default="0.0.0.0", type=str, help="Service host")
    parser.add_argument("--port", default=8002, type=int, help="Service port")
    parser.add_argument("--lang", default="cn", type=str, help="Language")
    parser.add_argument("--model_format", default="internlm_server", type=str, help="Model format")
    parser.add_argument("--search_engine", default="BingSearch", type=str, help="Search engine")
    parser.add_argument("--asy", default=False, action="store_true", help="Agent mode")

    return parser.parse_args()

args = parse_arguments() 
app = FastAPI() 

app.add_middleware(
    CORSMiddleware, 
    allow_orgins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

class GenerationParams(BaseModel):
    inputs: Union[str, List[Dict]]
    session_id: int = Field(default_factory=lambda: random.randint(0, 999999))
    agent_cfg: Dict = dict() 

def _postprocess_agent_message(message: dict) -> dict:
    pass 


async def run(request: GenerationParams, _request: Request):
    async def generate():
        try:
            queue = janus.Queue() 
            stop_event = asyncio.Event() 

    inputs = request.inputs 
    session_id = request.session_id 
    agent = init_agent(
        lang=args.lang, 
        model_format=args.model_format,
        search_engine=args.search_engine,
    )    

    return EventSourceResponse(generate(), ping=30)
