import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

from preprocess import preprocess_text
from vocab import build_vocab
from dataset import SpamDataset
from model import SpamClassifier
import json
from vocab import text_to_sequence, pad_sequence
from torch.utils.data import WeightedRandomSampler


# -------------------------------
# Load dataset
# -------------------------------


def load_data(path):
    df = pd.read_csv(path)
    return df


# -------------------------------
# Convert labels: ham/spam → 0/1
# -------------------------------
def encode_labels(df):
    df['label'] = df['label'].str.strip()
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    return df


# -------------------------------
# Main training pipeline
# -------------------------------
def main():

    # 1. Load data
    df = load_data("../data/processed/spam.csv")

    # 2. Encode labels
    df = encode_labels(df)

    # 3. Clean text
    df = preprocess_text(df)

    # 4. Build vocabulary
    vocab = build_vocab(df['message'])
    print("Vocab size:", len(vocab))

    # 5. Train/Test split (IMPORTANT)
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label'], test_size=0.2, random_state=42
    )

    train_texts = X_train.tolist()
    train_labels = y_train.tolist()

    test_texts = X_test.tolist()
    test_labels = y_test.tolist()

    # 6. Config
    max_len = 20
    batch_size = 32
    embed_dim = 128
    num_epochs = 15

    labels = train_labels  # already list of 0/1

    class_counts = [len([l for l in labels if l == 0]),
                    len([l for l in labels if l == 1])]

    weights = [1.0 / class_counts[label] for label in labels]

    sampler = WeightedRandomSampler(
        weights, num_samples=len(weights), replacement=True)
    # 7. Dataset
    train_dataset = SpamDataset(train_texts, train_labels, vocab, max_len)
    test_dataset = SpamDataset(test_texts, test_labels, vocab, max_len)

    # 8. DataLoader
    # train_loader=DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, sampler=sampler)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    # 9. Model
    vocab_size = len(vocab)
    model = SpamClassifier(vocab_size, embed_dim)
    # count labels
    num_spam = sum(train_labels)
    num_ham = len(train_labels) - num_spam

    print("Ham:", num_ham, "Spam:", num_spam)

    # compute weight
    pos_weight = torch.tensor([num_ham / num_spam])
    # 10. Loss + Optimizer
    # criterion = nn.BCEWithLogitsLoss()
    # criterion=nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # -------------------------------
    # 11. Training loop
    # -------------------------------
    for epoch in range(num_epochs):
        model.train()  # set model to training mode
        total_loss = 0

        for X_batch, y_batch in train_loader:
            # forward pass
            outputs = model(X_batch)

            # compute loss
            loss = criterion(outputs, y_batch)

            # clear gradients
            optimizer.zero_grad()

            # backpropagation
            loss.backward()

            # update weights
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    # -------------------------------
    # 12. Evaluation (on test data)
    # -------------------------------
    model.eval()  # evaluation mode

    correct = 0
    total = 0

    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            outputs = model(X_batch)

            # convert logits → probability → class
            predictions = torch.sigmoid(outputs) >= 0.5

            correct += (predictions.float() == y_batch).sum().item()
            total += y_batch.size(0)

    accuracy = correct / total
    print(f"Test Accuracy: {accuracy:.4f}")

    # ===============================
    # 🔥 13. SANITY CHECK
    # ===============================
    sample_text = "free entry win money now"

    cleaned = sample_text
    sequence = text_to_sequence(cleaned, vocab)
    padded = pad_sequence(sequence, max_len)

    input_tensor = torch.tensor([padded], dtype=torch.long)

    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
        prob = torch.sigmoid(output).item()

        # ✅ print INSIDE block
        print("Logit:", output.item())
        print("Probability:", prob)

    print("TRAIN CHECK →", sample_text, prob)

    # -------------------------------
    # 13. save model
    # -------------------------------
    # torch.save(model.state_dict(), "../model/model.pt")
    torch.save({
        "model_state": model.state_dict(),
        "vocab": vocab,
        "embed_dim": embed_dim
    }, "../model/model_full.pt")

    print("Model saved!")
   # -------------------------------
   # 14. Save vocab
   # -------------------------------
    with open("../model/vocab.json", "w") as f:
        json.dump(vocab, f)

    print("Vocab saved!")


# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    main()
