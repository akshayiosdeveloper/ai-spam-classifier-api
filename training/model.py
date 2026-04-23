import torch
import torch.nn as nn


class SpamClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)

        self.lstm = nn.LSTM(embed_dim, 64, batch_first=True)

        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        embedded = self.embedding(x)              # [batch, seq, embed]

        _, (hidden, _) = self.lstm(embedded)      # hidden: [1, batch, 64]

        out = self.fc(hidden[-1])                 # [batch, 1]

        return out.squeeze(1)
