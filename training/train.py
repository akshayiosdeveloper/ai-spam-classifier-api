import pandas as pd
from preprocess import preprocess_text

def load_data(path):
    df = pd.read_csv(path)
    return df

def encode_labels(df):
    df['label'] = df['label'].str.strip()
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})
    return df

def main():
    df = load_data("../data/processed/spam.csv")
    
    df = encode_labels(df)
    df = preprocess_text(df)
    
    print(df.head())
    
    print(df['label'].value_counts())
    
if __name__ == "__main__":
    main()    