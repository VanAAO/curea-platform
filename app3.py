from flask import Flask, request, jsonify
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER model for sentiment analysis
nltk.download('vader_lexicon')

app = Flask(__name__)

# Load trained NLP model
nlp = spacy.load("trained_nlp_model")

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Define response mapping
services = {
    "financial_support": {
        "name": "Citizens Advice Scotland",
        "description": "Help with claiming Universal Credit and financial aid.",
        "phone": "0800 023 2581",
        "website": "https://www.citizensadvice.org.uk/"
    },
    "mental_health": {
        "name": "Breathing Space",
        "description": "Confidential support for those experiencing low mood or anxiety.",
        "phone": "0800 83 85 87",
        "website": "http://breathingspace.scot/"
    },
    "employment": {
        "name": "ABZWorks",
        "description": "Support for employment, education, and training.",
        "website": "https://abzworks.co.uk/"
    }
}

# Store user session data
user_sessions = {}


# Function to analyze sentiment
def analyze_sentiment(user_input):
    scores = sentiment_analyzer.polarity_scores(user_input)
    sentiment = "neutral"
    if scores["compound"] >= 0.5:
        sentiment = "positive"
    elif scores["compound"] <= -0.5:
        sentiment = "negative"
    return sentiment


# Function to predict multiple intents
def predict_intents(user_input):
    doc = nlp(user_input)
    scores = doc.cats
    threshold = 0.5

    detected_intents = {intent: score for intent, score in scores.items() if score >= threshold}

    return detected_intents


# Function to generate warm, empathetic responses
def generate_response(user_id, user_input):
    session = user_sessions.get(user_id, {"step": 0, "intents": [], "sentiment": "neutral"})

    # Detect sentiment
    sentiment = analyze_sentiment(user_input)
    session["sentiment"] = sentiment

    # Detect user intent
    if session["step"] == 0:
        session["intents"] = predict_intents(user_input)
        user_sessions[user_id] = session

        if not session["intents"]:
            return "I want to help, but I need a bit more detail. Are you struggling financially, emotionally, or with job-related matters?"

        # Adjust response based on sentiment
        if sentiment == "negative":
            response = "I'm really sorry you're feeling this way. You're not alone, and I'm here to help. "
        elif sentiment == "positive":
            response = "That sounds promising! Let's see how I can assist you. "
        else:
            response = "Thanks for sharing. I'll do my best to guide you. "

        # Financial Support
        if "financial_support" in session["intents"]:
            session["step"] = 1
            return response + "Are you currently receiving any income or government support?"

        # Mental Health
        if "mental_health" in session["intents"]:
            session["step"] = 2
            return response + "Have you spoken to anyone about how you're feeling?"

        # Employment
        if "employment" in session["intents"]:
            session["step"] = 3
            return response + "Are you looking for training, job listings, or career advice?"

    # Step 2: Follow-up Questions
    if session["step"] == 1:  # Financial Support
        session["step"] = 4
        return "That’s tough. I can connect you with financial aid services. Would you like emergency grants or long-term support?"

    if session["step"] == 2:  # Mental Health
        session["step"] = 5
        return "It’s okay to not be okay. Would you prefer a helpline or an online chat service?"

    if session["step"] == 3:  # Employment
        session["step"] = 6
        return "Got it. What kind of job are you looking for?"

    # Final step: Provide resources
    if session["step"] in [4, 5, 6]:
        services_list = [services[intent] for intent in session["intents"]]
        response = "Here’s what I found for you:\n"
        for service in services_list:
            response += f"📌 **{service['name']}**\n   {service['description']}\n   📞 {service['phone']}\n   🌍 [Visit Website]({service['website']})\n\n"

        session["step"] = 0  # Reset conversation
        return response

    return "I'm here to help. Can you tell me more about what's going on?"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    user_id = data.get("user_id", "default_user")  # Simulate user tracking

    response = generate_response(user_id, user_input)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
