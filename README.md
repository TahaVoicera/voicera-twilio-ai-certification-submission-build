# voicera-twilio-ai-certification-submission-build
This repository contains the submission build for Twilio AI Certification. The build contains Twilio services: ConversationRelay and ConversationIntelligence to leverage AI Voice agent capabilities.

Refer the "_Conversation Intelligence Service Config Screenshots_" folder for screenshots of Conversational Intelligence Service Configuration with operators (built-in and custom). 

For **Conversational Intelligence** Service, the operators list is as follows:
- Built-in operators:
  Escalation Request, Agent Introduction, Call Transfer, Entity Recognition, Conversation Summary, Sentiment Analysis.
- Custom Operator:
  Service Classifier (Uses fuzzy phrase matching to find which service was called)

  <img width="1416" height="807" alt="image" src="https://github.com/user-attachments/assets/94f69cc0-282a-4061-be76-d52ba3db34db" />

For **ConversationRelay**:
A _configurations.py_ file is used which contains welcome message, speech-to-text configurations, text-to-speech-configurations.

**System Diagram:**
<img width="1920" height="1080" alt="ConversationRelay" src="https://github.com/user-attachments/assets/62b62922-aad4-468e-9ad3-ba997e2fcab7" />

**Application Flow / Design:**
1. A Twilio number is webhooked to the /call endpoint in _app.py_.
2. Once a call is received, a TwiML is generated using the welcome message, **intelligenceService** stt, tts configs present in the _configurations.py_ file.
3. A welcome message is played and the conversation is now handled by the **ConversationRelay** Websocket Pipeline (_/relay websocket endpoint_).
4. The _chat_service.py_ file handles the **ConversationRelay** flow which contains call setup, user prompt and interruption handling.
5. User queries are then passed to _chat_wrapper.py_ which performs LLM calls to fetch data from document (knowledge base). For query retrieval, we have implemented simple CAG (Cache Augmented Generation) but it can also be implemented using RAG (Retrieval Augmented Generation) or KAG (Knowledge Augmented Generation).
6. We stream the LLM response back to the ConversationRelay websocket which then plays the response to user.
7. The conversation transcript is sent to **ConversationalIntelligence** Service using the intelligenceService attribute in the ConversationRelay TwiML which then provides the insights mentioned in the operators list (sentiment analysis, summarization, etc...)

**Insights Generated**
<img width="1902" height="910" alt="image" src="https://github.com/user-attachments/assets/55579d5f-a2c4-4de4-8a92-6cd098ac48eb" />


How to run the code?
1. Pull the repository
3. In terminal : pip install fastapi uvicorn dotenv groq websockets
4. In .env file enter NGROK_URL , GROQ_API_KEY TWILIO_CONVERSATIONAL_INTELLIGENCE_SID
5. Generate a ngrok url for http 8080 and link it to voice calls webhook for your Twilio number (using console or API)
6. In terminal: _python app.py_
