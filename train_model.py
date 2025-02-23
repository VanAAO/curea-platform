import spacy
from spacy.training.example import Example

# Load a medium-sized spaCy model
nlp = spacy.load("en_core_web_md")

# Define training data with multiple intents
TRAINING_DATA = [
    ("I lost my job and need financial help", {"cats": {"financial_support": 1.0, "employment": 1.0, "mental_health": 0.0}}),
    ("How do I apply for universal credit?", {"cats": {"financial_support": 1.0, "employment": 0.0, "mental_health": 0.0}}),
    ("I feel really anxious and can't sleep", {"cats": {"mental_health": 1.0, "financial_support": 0.0, "employment": 0.0}}),
    ("I'm struggling financially and feeling depressed", {"cats": {"financial_support": 1.0, "mental_health": 1.0, "employment": 0.0}}),
    ("I need help finding a job", {"cats": {"financial_support": 0.0, "mental_health": 0.0, "employment": 1.0}}),
    ("I lost my job and it's making me feel stressed", {"cats": {"financial_support": 1.0, "mental_health": 1.0, "employment": 1.0}}),
]

# Add text classification pipeline
if "textcat" not in nlp.pipe_names:
    textcat = nlp.add_pipe("textcat_multilabel", last=True,)  # Multi-label classification
else:
    textcat = nlp.get_pipe("textcat")

# Add labels to the text classifier
for intent in ["financial_support", "mental_health", "employment"]:
    textcat.add_label(intent)

# Training loop
optimizer = nlp.begin_training()
for epoch in range(20):  # Adjust number of epochs as needed
    losses = {}
    for text, annotations in TRAINING_DATA:
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], losses=losses)
    print(f"Losses at epoch {epoch}: {losses}")

# Save the model
nlp.to_disk("trained_nlp_model")
print("Multi-intent model training complete and saved.")
