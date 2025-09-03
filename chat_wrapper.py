import asyncio
import json
import os
from typing import Optional
import time
import openai
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, Response
from fastapi.websockets import WebSocketState
from groq import Groq
import logging 

logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

async def stream_llm_response(client, messages, websocket, model):
    """Stream LLM response and handle tool calls during streaming"""
    collected_content = ""
    collected_tool_calls = []
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            reasoning_format="hidden",
        )
        
        # Collect streaming response and tool calls
        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                
                # Handle content streaming
                if delta and delta.content:
                    token = delta.content
                    # Stream each token to the websocket
                    await websocket.send_text(
                        json.dumps({
                            "type": "text", 
                            "token": token,
                            "last": False
                        })
                    )
                    collected_content += token
                        
        # Send final message to indicate streaming is complete
        await websocket.send_text(
            json.dumps({
                "type": "text",
                "token": "",
                "last": True
            })
        )
        logger.info(f"{GREEN}Agent Response : {collected_content}{RESET}")
        return collected_content, messages
        
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        return "", messages