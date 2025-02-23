from flask import Flask, request, jsonify, render_template
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import random

# Download VADER model for sentiment analysis
nltk.download('vader_lexicon')

app = Flask(__name__)

# Load trained NLP model
nlp = spacy.load("trained_nlp_model")

# Initialize sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Serve the frontend
@app.route("/")
def home():
    return render_template("ai-convo.html")

financial_issues_responses = [
    "I understand this might be a tough topic. Are you currently receiving any income or government support?",
    "It sounds like you're going through a lot. Do you have any income or government assistance at the moment?",
    "Financial struggles can be overwhelming. Are you getting any financial help, like benefits or support from the government?",
    "I’m here to help. Do you currently receive any income or benefits?",
    "Let’s see how we can improve your situation. Are you on any government support programs or receiving income right now?"
]

mental_health_responses = [
    "I understand this might be difficult to talk about. Have you spoken to anyone about how you're feeling?",
    "It sounds like you're going through a lot. It’s important to share how you’re feeling. Have you talked to someone about this?",
    "Mental health struggles can feel overwhelming. Talking about your feelings can help. Have you reached out to anyone?",
    "I’m here to help. Have you shared your thoughts or feelings with someone you trust?",
    "It’s okay to ask for help. Have you spoken to a friend, family member, or professional about how you’re feeling?"
]

employment_responses = [
    "I understand job-related challenges can be tough. Are you looking for training, job listings, or career advice?",
    "It sounds like you're exploring your options. What kind of job support are you looking for? Training, job listings, or advice?",
    "Finding the right job can be challenging. Are you interested in training opportunities, job openings, or guidance for your career?",
    "I’m here to help. What area of employment support do you need? Training, job listings, or career advice?",
    "Let’s see how we can improve your job situation. Are you searching for training programs, job opportunities, or career guidance?"
]

low_mood_responses =[
    "I understand this might be difficult to talk about. Have you spoken to anyone about how you're feeling?",
    "It sounds like you're going through a lot. It’s important to share how you’re feeling. Have you talked to someone about this?",
    "Low mood can feel overwhelming. Talking about your feelings can help. Have you reached out to anyone?",
    "I’m here to help. Have you shared your thoughts or feelings with someone you trust?",
    "It’s okay to ask for help. Have you spoken to a friend, family member, or professional about how you’re feeling?"
]

welfare_fund_responses = [
     "I understand financial struggles can be overwhelming. Are you currently receiving any income or government support?",
    "It sounds like you're going through a tough time. Do you have any income or government assistance at the moment?",
    "Financial challenges can feel isolating. Are you getting any financial help, like benefits or support from the government?",
    "I’m here to help. Do you currently receive any income or benefits?",
    "Let’s see how we can improve your situation. Are you on any government support programs or receiving income right now?"
]

conflict_resolution_responses =[
    "Conflict can be tough to navigate. Have you tried talking to the other person about how you feel?",
    "It sounds like this situation is really challenging. It’s important to communicate openly. Have you discussed the issue with them?",
    "I’m here to help. Would you like help finding a way to resolve this conflict?",
    "Sometimes a neutral third party can help. Have you considered mediation or talking to a neutral third party?",
    "Do you think the other person would be open to resolving this together? Let’s explore how we can make that happen."
]

# Define response mapping
services = {
    "financial_issue": {
        "name": "Citizens Advice Scotland",
        "description": "Help with claiming Universal Credit and financial aid.",
        "phone": "0800 023 2581",
        "website": "https://www.citizensadvice.org.uk/"
    },
    "mental_health": {
        "name": "Breathing Space",
        "description": "Confidential support for those experiencing low mood or anxiety.",
        "phone": "0800 83 85 87",
        "website": "http://breathingspace.scot/",
    },
    "employment": {
        "name": "ABZWorks",
        "description": "Support for employment, education, and training.",
        "phone": "0800 83 85 87",
        "website": "https://abzworks.co.uk/"
    },
    "low_mood": {
        "name": "Scottish Action for Mental Health",
        "description": "Support for people experiencing low mood and mental health challenges.",
        "phone": "0344 800 0550",
        "website": "https://samh.org.uk/informationservice"
    },
    "welfare_fund": {
        "name": "Scottish Welfare Fund",
        "description": "Help with crisis grants and community care grants.",
        "phone": "0800 028 1456",
        "website": "https://www.mygov.scot/scottish-welfare-fund/"
    },
    "conflict_resolution": {
        "name": "Scottish Centre for Conflict Resolution",
        "description": "Mediation services for conflict resolution in various areas.",
        "website": "https://www.scottishconflictresolution.org.uk/"
    }
}

# Store user session data
user_sessions = {}

# Function to analyze sentiment
def analyze_sentiment(user_input):
    scores = sentiment_analyzer.polarity_scores(user_input)
    sentiment = "neutral"
    if scores["compound"] >= 0.3:
        sentiment = "positive"
    elif scores["compound"] <= -0.3:
        sentiment = "negative"
    return sentiment

# Function to predict multiple intents
def predict_intents(user_input):
    doc = nlp(user_input)
    scores = doc.cats
    threshold = 0.3
    detected_intents = {intent: score for intent, score in scores.items() if score >= threshold}
    return detected_intents

# Function to generate warm, empathetic responses
def generate_response(user_id, user_input):
    # Initialize or retrieve session
    session = user_sessions.get(user_id, {"step": 0, "intents": [], "sentiment": "neutral"})

    # Handle greetings
    if user_input.lower().strip() in ["hello", "hii", "hi", "hey"]:
        return "Hello! How are you?"
    elif user_input.lower().strip() in ["i'm fine", "i'm doing well", "i'm doing good", "fine"]:
        return "That's great to hear! How can I help you?"
    elif user_input.lower().strip() in ["not good", "i'm bad", "i'm not well"]:
        return "I'm sorry to hear that. How can I assist you?"

    # Detect sentiment
    sentiment = analyze_sentiment(user_input)
    session["sentiment"] = sentiment

    # Detect user intent
    if session["step"] == 0:
        session["intents"] = list(predict_intents(user_input).keys())
        user_sessions[user_id] = session

        if not session["intents"]:
            return "I'm here to help. Could you share a bit more about what you're going through? Are you facing financial difficulties, emotional challenges, job-related concerns, or having disagreement?"
        
        # Adjust response based on sentiment
        if sentiment == "negative":
            response = "I'm really sorry you're feeling this way. You're not alone, and I'm here to help. "
        elif sentiment == "positive":
            response = "That sounds promising! Let's see how I can assist you. "
        else:
            response = "Thanks for sharing. I'll do my best to guide you. "

        # Financial Support
        if "financial_issue" in session["intents"]:
            session["step"] = 1
            user_sessions[user_id] = session
            return response + + random.choice(financial_issues_responses)

        # Mental Health
        if "mental_health" in session["intents"]:
            session["step"] = 2
            user_sessions[user_id] = session
            return response + random.choice(mental_health_responses)
        # Employment
        if "employment" in session["intents"]:
            session["step"] = 3
            user_sessions[user_id] = session
            return response + random.choice(employment_responses)
        
        #low mood
        if "low_mood" in session["intents"]:
            session["step"] = 4
            user_sessions[user_id] = session
            return response + random.choice(low_mood_responses)
        
        #welfare_fund
        if "welfare_fund" in session["intents"]:
            session["steps"] = 5
            user_sessions[user_id] = session
            return response + random.choice(welfare_fund_responses)
        
        #conflict_resolution
        if "conflict_resolution" in session["intents"]:
            session["steps"] = 6
            user_sessions[user_id] = session
            return response + random.choice(conflict_resolution_responses)
            
        
    # Step 2: Follow-up Questions
    if session["step"] == 1:  # Financial issue
        session["step"] = 7
        user_sessions[user_id] = session
        return "That’s tough. I can connect you with financial aid services. Would you like emergency grants or long-term support?"

    if session["step"] == 2:  # Mental Health
        session["step"] = 8
        user_sessions[user_id] = session
        return "It’s okay to not be okay. Would you prefer a helpline or an online chat service?"

    if session["step"] == 3:  # Employment
        session["step"] = 9
        user_sessions[user_id] = session
        return "Got it. What kind of job are you looking for?"
    
    if session["step"] == 4:  # low_mood
        session["step"] = 10
        user_sessions[user_id] = session
        return "Would you like me to help you find someone to talk to, like a counselor or therapist?"
    
    if session["step"] == 5:  # welfare_fund
        session["step"] = 11
        user_sessions[user_id] = session
        return "Would you like information about local resources that could help with your situation?"
    
    if session["step"] == 6:  # conflict_resolution 
        session["step"] = 12
        user_sessions[user_id] = session
        return "Would you be open to trying mediation or conflict resolution services?"

    # Final step: Provide resources
    if session["step"] in [7, 8, 9, 10, 11, 12]:
        services_list = []
        for intent in session["intents"]:
            if intent in services:
                services_list.append(services[intent])

        response = "Here’s what I found for you:\n"
        for service in services_list:
            name = service.get('name', 'Unknown Service')
            description = service.get('description', 'No description available')
            phone = service.get('phone', 'No phone number available')
            website = service.get('website', '#')

            response += f"📌 {name}\n   {description}\n   📞 {phone}\n   🌍 {website}\n\n"

        session["step"] = 0  # Reset conversation
        user_sessions[user_id] = session
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