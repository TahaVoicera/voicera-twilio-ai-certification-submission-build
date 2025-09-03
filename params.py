import os
from dotenv import load_dotenv
from configurations import config

load_dotenv()
DOMAIN = os.getenv("NGROK_URL")
SID = os.getenv("TWILIO_CONVERSATIONAL_INTELLIGENCE_SID")



def get_config():
    ws_url = f"wss://{DOMAIN}/relay"
    welcome = config.get("welcome_message") or "Hello! How can I help you today?"
    language = config.get("language")
    stt_provider = config.get("stt").get("provider")
    stt_model = config.get("stt").get("stt_model")
    tts_provider = config.get("tts").get("provider")
    voice = config.get("tts").get("voice_id")

    attrs_cr_noun = [f"url=\"{ws_url}\""]
    attrs_lang_noun = []

    attrs_cr_noun.append(f"welcomeGreeting=\"{welcome}\"")

    attrs_lang_noun.append(f"code=\"{language}\"")
    attrs_cr_noun.append(f"transcriptionLanguage=\"{language}\"")

    attrs_lang_noun.append(f"ttsProvider=\"{tts_provider}\"")
    attrs_cr_noun.append(f"ttsProvider=\"{tts_provider}\"")

    attrs_lang_noun.append(f"voice=\"{voice}\"")
    attrs_cr_noun.append(f"voice=\"{voice}\"")

    attrs_lang_noun.append(f"transcriptionProvider=\"{stt_provider}\"")
    attrs_cr_noun.append(f"transcriptionProvider=\"{stt_provider}\"")

    attrs_lang_noun.append(f"speechModel=\"{stt_model}\"")
    attrs_cr_noun.append(f"speechModel=\"{stt_model}\"")

    return attrs_cr_noun, attrs_lang_noun


