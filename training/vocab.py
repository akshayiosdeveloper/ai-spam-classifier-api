from collections import Counter


def build_vocab(texts, min_freq=2):
    counter = Counter()

    # count words
    for text in texts:
        words = text.split()
        counter.update(words)

    vocab = {"<PAD>": 0, "<UNK>": 1}
    for word, freq in counter.items():
        # print("word: ", word + " " + "freq: ", freq)
        if freq >= min_freq:
            vocab[word] = len(vocab)

    print(list(vocab.items())[:10])
    return vocab


def text_to_sequence(text, vocab):
    words = text.split()

    sequence = []

    for word in words:
        if word in vocab:
            sequence.append(vocab[word])
        else:
            sequence.append(vocab["<UNK>"])

    return sequence


def pad_sequence(sequence, max_len):
    if len(sequence) < max_len:
        sequence = sequence + [0] * (max_len - len(sequence))
    else:
        sequence = sequence[:max_len]

    return sequence
