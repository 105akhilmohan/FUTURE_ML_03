import os
import pandas as pd
import google.generativeai as genai
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Load dataset
faq_data = pd.read_csv("sample.csv")

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyAgcI_ldwbQpvcacEIUAlF1bCrTYbG1vLg"))

class ActionAnswerFromCSV(Action):
    def name(self) -> str:
        return "action_ask_gemini"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        user_message = tracker.latest_message.get("text").lower()
        
        # Try CSV lookup first
        answer = None
        for _, row in faq_data.iterrows():
            if row['question'].lower() in user_message:
                answer = row['answer']
                break
        
        # If not found, use Gemini as fallback
        if not answer:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(user_message)
            answer = response.text

        dispatcher.utter_message(text=answer)
        return []