import os
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from dotenv import load_dotenv
import logging 

from params import get_config
from chat_service import process_chat

load_dotenv()

app = FastAPI()

PORT = int(os.getenv("PORT", "8080"))
CI_SID = os.getenv("TWILIO_CONVERSATIONAL_INTELLIGENCE_SID")

logging.basicConfig(
    level=logging.INFO,  # Minimum level to log
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@app.post("/call")
async def call_webhook():
    """Endpoint that returns TwiML for Twilio to connect to the WebSocket. This endpoint is a webhook to a Twilio phone number."""

    attrs_cr_noun, attrs_lang_noun = get_config()

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Connect>
        <ConversationRelay {' '.join(attrs_cr_noun)} interruptible="speech" intelligenceService="{CI_SID}">
            <Language {' '.join(attrs_lang_noun)} />
        </ConversationRelay>
      </Connect>
    </Response>"""
    
    return Response(content=xml_response, media_type="text/xml")

@app.websocket("/relay")
async def websocket_endpoint(websocket : WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    logger.info("Control transferred to websocket connected with app.")

    try:
        await process_chat(websocket)
    except WebSocketDisconnect:
        logger.info(f"TCR WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Error in TCR websocket: {str(e)}")    




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
    print(f"Server running at http://localhost:{PORT} ")

