import csv
import pandas as pd

with open('ngrams_words_5.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('ngrams_words_5.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('title', 'intro'))
        writer.writerows(lines)


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('ngrams_words_5.csv')
df_split = df['title'].str.split('\t', expand=True)

# List of words to filter out
words_to_remove = ['of', 'the', 'and', 'is', 'to', 'I', 'do', 'as', 'a', 'wo', 'so', 'If', 'you', 'are', 'be', 'a', 'was', 'it', 'me', 'if']
#'in', 'he', 'she', 'an', 'that', 'The', 'this', 'at', 'for', 'this', 'that', 'does', 'we', 'us', 'He', 'She', 'or', 'can',"n't", "have", 'been', 'no', 'by', 'they', 'not', 'on', 'than', 'am', 'your', 'will', 'more', 'from'

# Create a mask that checks if any cell contains any of the words
mask = df_split.applymap(lambda x: str(x).lower() in {word.lower() for word in words_to_remove})

# Drop rows where any cell contains the specific words
df_cleaned = df_split[~mask.any(axis=1)]

# Display the first few rows of the dataframe
print(df_cleaned.head())
df_cleaned.to_csv('ngram5-2.csv', index=False)