import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("No GEMINI_API_KEY found in environment or .env file.")
else:
    print(f"Testing LangChain Gemini API Key ending in: ...{key[-5:] if len(key) >= 5 else '***'}")

for model_name in ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest"]:
    print(f"\nTrying model: {model_name}...")
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name, 
            google_api_key=key, 
            temperature=0.3
        )
        messages = [HumanMessage(content="Say hello in one word.")]
        response = llm.invoke(messages)
        print(f"Success with {model_name}! Response: {response.content}")
        break
    except Exception as e:
        print(f"Failed with {model_name}: {str(e)}")
