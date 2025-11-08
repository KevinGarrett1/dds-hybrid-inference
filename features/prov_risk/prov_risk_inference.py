# prov_risk_inference.py
# This script loads a trained model and computes a "provocation risk" score for a given text.
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Path to your fine‑tuned model directory
model_path = "/content/prov_risk_model"

# Load the trained classification model from the saved directory
prov_model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Load a base tokenizer (BERT tokenizer) to convert text into model‑readable tokens
prov_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")



def compute_prov_risk(text):
     # take in some text and return a risk score between 0 and 1
    # basically how “provocative” or risky the text might be

    
    # tokenize the text so the model can read it
    enc = prov_tokenizer(text, return_tensors='pt', truncation=True, padding=True)

     # no gradients needed since we’re just running inference, not training
    with torch.no_grad():
             # get the raw model outputs (logits)
        preds = prov_model(**enc).logits

          # turn logits into probabilities 
    probs = torch.nn.functional.softmax(preds, dim=1)

      # add up the probabilities for classes 1 and 2 (assuming those mean “risky”)
    prov_risk = float((probs[:,1] + probs[:,2]).item())

      # return that number so we can print or use it later
    return prov_risk


# just a quick test example
sample_text = "There’s a bomb at the downtown station!"

# run the function on the sample text
score = compute_prov_risk(sample_text)


# print out the result so we can see what the model thinks
print({"text": sample_text, "prov_risk": score})
