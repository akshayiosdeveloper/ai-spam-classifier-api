import os
from fastapi import FastAPI
import torch
import json

from training.model import SpamClassifier
from training.vocab import text_to_sequence, pad_sequence
from training.preprocess import clean_text
from pydantic import BaseModel

app = FastAPI()
print("Model path exists:", os.path.exists("model/model.pt"))


class MessageRequest(BaseModel):
    message: str


# load vocab
with open("model/vocab.json", "r") as f:
    vocab = json.load(f)

# config (must match training)
checkpoint = torch.load("model/model_full.pt", map_location="cpu")
vocab = checkpoint["vocab"]
embed_dim = checkpoint["embed_dim"]
max_len = 20

# recreate model
model = SpamClassifier(len(vocab), embed_dim)
# load weights
model.load_state_dict(checkpoint["model_state"])

model.eval()


@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}


@app.post("/predict")
def predict(request: MessageRequest):
    text = request.message

    # 1. clean text
    text = clean_text(text)

    # 2. text → sequence
    sequence = text_to_sequence(text, vocab)

    # 3. padding
    padded = pad_sequence(sequence, max_len)

    # 4. convert to tensor
    input_tensor = torch.tensor([padded], dtype=torch.long)

    # 5. model prediction
    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output / 2).item()

    # 6. decision
    prediction = "spam" if prob >= 0.5 else "ham"
    # ✅ 7. confidence (important)
    confidence = prob if prediction == "spam" else 1 - prob

    # ✅ 8. level (ADD HERE)
    if confidence > 0.9:
        level = "High"
    elif confidence > 0.7:
        level = "Medium"
    else:
        level = "Low"
    print("----- DEBUG -----")
    print("Input:", request.message)
    print("Clean:", text)
    print("Sequence:", sequence)
    print("Prediction prob:", prob)
    print("-----------------")

    print("free index:", vocab.get("free"))
    print("win index:", vocab.get("win"))
    print("money index:", vocab.get("money"))
    print("-----------------")
    print(vocab.get("free"))
    print(vocab.get("win"))
    print(vocab.get("money"))
    # 9. response
    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "level": level
    }
