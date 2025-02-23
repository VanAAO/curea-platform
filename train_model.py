import spacy
from spacy.training.example import Example
from spacy.matcher import Matcher
import json

# Load spaCy model with necessary components
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Define Matcher with a pattern
matcher = Matcher(nlp.vocab)
pattern = [
    {"LOWER": "hello"},
    {"IS_PUNCT": True, "OP": "?"},
    {"LOWER": "how"},
    {"LOWER": "are"},
    {"LOWER": "you"}
]
matcher.add("GREETING_PATTERN", [pattern])


def preprocess_text(text):
    if isinstance(text, tuple):  # Unpack tuple if needed
        text = text[0]
    text = str(text)  # Ensure input is a string
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])  # Return lemmatized text

# Define training data with multiple intents
TRAINING_DATA = [
    ("I am broke", {"cats": {"financial_issue": 1.0, "mental_health": 0.0,
     "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("I dont have money", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("What should I do if I’m struggling to complete my Universal Credit claim?", {"cats": {
     "financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("How can I check if I’m eligible for Universal Credit?", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("Where can I find support to set up an email or bank account for my claim?", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("I am feeling very sad",
     {"cats": {"financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("What support is available if I need financial help before my first Universal Credit payment?", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("How do I prepare for my Universal Credit work coach appointment?", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("Where can I call for free advice about my Universal Credit claim?", {"cats": {
     "financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I make sure all my claim evidence is correct?",
     {"cats": {"financial_issue": 1.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("Where can I find a safe space to talk about my mental health struggles?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("I am feeling depressed",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are some mindfulness techniques to reduce anxiety?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I improve my self-esteem and confidence?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What relaxation exercises can help me manage stress?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find emotional support if I feel overwhelmed?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can breathing exercises help with panic attacks?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are some holistic approaches to managing mental health?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I practice self-care when I’m feeling low?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What techniques can help me overcome negative thoughts?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I deal with loneliness and isolation?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find support for healing from trauma?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are some ways to cope with intrusive thoughts?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I stop overthinking and learn to relax?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I create a daily routine that improves my mental health?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are some simple ways to practice gratitude and mindfulness?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find guided meditation for stress relief?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I stay positive during difficult times?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What can I do if I feel constantly anxious?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I manage anger in a healthy way?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I deal with emotional numbness or burnout?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are the benefits of breathwork and yoga for mental health?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I get help for intrusive thoughts and OCD?",
     {"cats": {"financial_issue": 0.0, "mental_health": 1.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find support to gain confidence and skills for employment?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I get help finding a job if I have no experience?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find training programs to improve my job prospects?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I switch careers and gain new skills?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I get help with my CV and job applications?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What support is available for people returning to work after a break?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I find local job opportunities in Aberdeen?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find support if I’ve been made redundant?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What services help people over 50 find work or retrain?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I find apprenticeship or work experience programs?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I access employment support if I have a disability?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What support is available for young people looking for their first job?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I prepare for job interviews and build confidence?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find employment support for single parents?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I improve my digital skills for the job market?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find support if I’m struggling to find work due to my background?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I get career advice tailored to my experience level?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 1.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I talk to someone about feeling low and unmotivated?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I find support when I'm feeling down but don’t know who to talk to?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I get emotional support for myself or a loved one struggling with low mood?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Is there a free service where I can chat with someone about my mood and emotions?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What should I do if I feel persistently sad and don’t know how to cope?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find information about mental health struggles and how to manage them?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I get help when I feel overwhelmed but don’t know where to start?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Is there an online chat service where I can get mental health support?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What resources are available for someone struggling with mood swings or sadness?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I support a friend or family member who is feeling low?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),
    ("How do I cope with feelings of loneliness and isolation?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I talk to someone about feeling alone and disconnected from others?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I deal with the pain of losing someone I love?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What should I do if I feel like I have no friends or support system?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I heal from a breakup and move forward emotionally?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I rebuild my self-esteem after being in a toxic relationship?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I get support when I feel like nobody understands me?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I cope with feeling unloved or unimportant in my relationships?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What can I do if I feel like I'm always giving in relationships but never receiving support?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How do I deal with feeling abandoned by my friends or family?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What are some healthy ways to process feelings of heartbreak?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("Where can I find emotional support after losing a close friend?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I open up about my emotions without feeling like a burden to others?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("What steps can I take to build deeper, more meaningful connections?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 1.0, "welfare_fund": 0.0, "conflict_resolution": 0.0}}),

    ("How can I apply for a crisis grant to cover emergency expenses?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("Where can I get financial help for food, heating, and other urgent needs?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("Am I eligible for a community care grant if I am moving into a new home?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("How do I get help with buying furniture or essential household items?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("What support is available for families under exceptional financial pressure?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("Can I get financial assistance if I am leaving homelessness or a temporary shelter?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("How many times can I apply for a crisis or community care grant in a year?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("What kind of expenses does the Scottish Welfare Fund cover?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("Where can I get help with essential costs if I have just been released from prison?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),

    ("Can I receive financial support if I am struggling after an emergency or disaster?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 1.0, "conflict_resolution": 0.0}}),
    ("How can I resolve conflicts with my parents or family members?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("Where can I get help if I keep arguing with my family at home?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("What should I do if I feel unsafe or uncomfortable due to family conflict?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("Are there online resources to help me deal with family arguments?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("How can I communicate better with my parents and avoid fights?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("What support is available for young people dealing with conflict at home?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("How do I handle disagreements with my family without making things worse?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

    ("Where can I find conflict resolution advice specifically for young people?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),
    ("What steps can I take to de-escalate conflicts with my family?",
     {"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),
    ("How can I get mediation support to help improve my relationship with my family?",{"cats": {"financial_issue": 0.0, "mental_health": 0.0, "employment": 0.0, "low_mood": 0.0, "welfare_fund": 0.0, "conflict_resolution": 1.0}}),

]

# Preprocess training data
processed_data = [preprocess_text(text) for text in TRAINING_DATA]

# Save processed data for training
with open("processed_training_data.json", "w") as f:
    json.dump(processed_data, f)

# Add text classification pipeline
if "textcat" not in nlp.pipe_names:
    textcat = nlp.add_pipe("textcat", last=True)
else:
    textcat = nlp.get_pipe("textcat")

# Add labels to the text classifier
labels = ["financial_issue", "mental_health", "employment", "low_mood", "welfare_fund", "conflict_resolution"]
for label in labels:
    textcat.add_label(label)

# Training loop
nlp.initialize()
for epoch in range(20):  # Adjust number of epochs as needed
    losses = {}
    for text, annotations in TRAINING_DATA:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], losses=losses)
    print(f"Losses at epoch {epoch}: {losses}")

# Save the model
nlp.to_disk("trained_nlp_model")
print("Multi-intent model training complete and saved.")
print("Training data preprocessed and saved successfully!")