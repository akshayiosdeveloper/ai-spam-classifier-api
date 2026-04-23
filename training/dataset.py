import torch
from torch.utils.data import Dataset

from preprocess import clean_text
from vocab import text_to_sequence, pad_sequence


class SpamDataset(Dataset):
    def __init__(self, texts, labels, vocab, max_len):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        # preprocess
        # text = clean_text(text)

        # text → sequence
        sequence = text_to_sequence(text, self.vocab)

        # padding
        padded = pad_sequence(sequence, self.max_len)

        # convert to tensor
        return (
            torch.tensor(padded, dtype=torch.long),
            torch.tensor(label, dtype=torch.float)
        )
