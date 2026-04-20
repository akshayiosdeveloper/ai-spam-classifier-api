import pandas as pd
import re

def load_data(path):
    df = pd.read_csv(path)
    return df

def encode_labels(df):
    df['label'] = df['label'].str.strip()
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    return df

def clean_text(text):
    text = text.lower()  # lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove special chars
    text = re.sub(r'\s+', ' ', text).strip()  # remove extra spaces
    return text

def preprocess_text(df):
    df['message'] = df['message'].apply(clean_text)
    return df

def main():
    df = load_data("../data/spam.csv")
    
    df = encode_labels(df)
    
    df = preprocess_text(df)
    
    print(df.head())
    
    print(df['label'].value_counts())
    
if __name__ == "__main__":
    main()    