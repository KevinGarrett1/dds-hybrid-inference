# this script shows how the ML team would save and later load the fine-tuned provocation risk model

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle

# assume we already fine-tuned a BERT model somewhere else
model_name = "bert-base-uncased"

# load the tokenizer and model (pretend this is your trained version)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# --- SAVE SECTION ---
# save the model and tokenizer into a single pickle file
# this makes it easy to share or upload to S3
save_path = "prov_risk_model.pkl"

# wrap both model and tokenizer together so we can reload them later
bundle = {
    "model_state_dict": model.state_dict(),
    "tokenizer": tokenizer
}

# write everything to a .pkl file
with open(save_path, "wb") as f:
    pickle.dump(bundle, f)

print(f"Model saved to {save_path}")

# --- LOAD SECTION ---
# later, when someone else needs to use it for inference
with open(save_path, "rb") as f:
    loaded_bundle = pickle.load(f)

# rebuild the model and load the weights
loaded_model = AutoModelForSequenceClassification.from_pretrained(model_name)
loaded_model.load_state_dict(loaded_bundle["model_state_dict"])
loaded_tokenizer = loaded_bundle["tokenizer"]

print("Model and tokenizer loaded successfully!")

# quick test to make sure everything works
text = "There’s a bomb at the downtown station!"
enc = loaded_tokenizer(text, return_tensors='pt', truncation=True, padding=True)
with torch.no_grad():
    preds = loaded_model(**enc).logits
probs = torch.nn.functional.softmax(preds, dim=1)
print("Predicted probabilities:", probs)