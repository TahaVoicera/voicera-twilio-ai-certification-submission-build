import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
import openai
from dotenv import load_dotenv
import logging
from params import get_config
from configurations import config
from chat_wrapper import stream_llm_response
from groq import Groq 
from knowledge_base import context
load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Basic logger setup
logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

async def process_chat(websocket: WebSocket):
    """Chat Processing Function that handles conversation relay setup, user prompts and interruptions."""
    SYSTEM_PROMPT = f"{config.get("system_prompt")}. Use this knowledge base : {context}"
    call_sid = None
    client = Groq(api_key=GROQ_API_KEY)
    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "setup":
                call_sid = message["callSid"]
                logger.info(f"Setup for call: {call_sid}")
                websocket.call_sid = call_sid
                
            elif message["type"] == "prompt":
                logger.info(f"{BLUE}User: {message['voicePrompt']}{RESET}")
                conversation.append({"role": "user", "content": message["voicePrompt"]})
                final_text, updated_conversation = await stream_llm_response(client= client, messages = conversation, websocket= websocket, model = "qwen/qwen3-32b")
                conversation = updated_conversation                
                conversation.append({"role": "assistant", "content": final_text})  
            elif message["type"] == "interrupt":
                logger.info(f"{YELLOW}Handling interruption.{RESET}")
                
            else:
                logger.info(f"Unknown message type received: {message['type']}")
                
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
        