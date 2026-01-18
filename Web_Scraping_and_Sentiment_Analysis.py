# %%
"""
Web Scraping and Sentiment Analysis Tool

This script scrapes text from URLs listed in an Excel file, performs sentiment analysis
and readability calculations, and outputs the results to a new Excel file.

Requirements:
- Input: 'input.xlsx' with columns 'URL_ID' and 'URL'
- Dictionaries: 'MasterDictionary/positive-words.txt' and 'negative-words.txt'
- Stop words: Files in 'StopWords/' directory
- Output: 'output.xlsx' with added metric columns, and text files in 'extracted_text/'

Usage:
1. Prepare 'input.xlsx' with URLs.
2. Run the script: python Web_Scraping_and_Sentiment_Analysis.py
3. Check 'output.xlsx' for results and 'extracted_text/' for saved texts.
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize, sent_tokenize
import re

# Load stop words from all .txt files in the StopWords directory
stop_words = set()
stopwords_directory = 'StopWords'
for filename in os.listdir(stopwords_directory):
    if filename.endswith('.txt'):
        with open(os.path.join(stopwords_directory, filename), encoding='ISO-8859-1') as file:
            stop_words.update([line.strip() for line in file])

# Load positive and negative word dictionaries
positive_words = set(line.strip() for line in open('MasterDictionary/positive-words.txt', encoding='ISO-8859-1'))
negative_words = set(line.strip() for line in open('MasterDictionary/negative-words.txt', encoding='ISO-8859-1'))

def extract_text_and_headings(html_content):
    """
    Extract plain text and headings from HTML content.

    Args:
        html_content (bytes): Raw HTML content from a webpage.

    Returns:
        tuple: (text, headings) where text is concatenated paragraph text,
               and headings is a list of heading texts.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in soup(['header', 'footer', 'img', 'iframe', 'media']):
        tag.extract()

    text = ' '.join([p.get_text() for p in soup.find_all('p')])
    headings = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    return text, headings

def scrape_url(url):
    """
    Scrape text and headings from a given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        tuple: (text, headings) if successful, (None, None) if failed.
    """
    response = requests.get(url)
    if response.status_code == 200:
        text, headings = extract_text_and_headings(response.content)
        return text, headings
    else:
        print(f"Failed to fetch URL: {url}")
        return None, None

def calculate_sentiment(text):
    """
    Calculate sentiment scores from text.

    Args:
        text (str): The text to analyze.

    Returns:
        tuple: (pos_score, neg_score, polarity, subjectivity)
               - pos_score: Count of positive words
               - neg_score: Count of negative words
               - polarity: Sentiment polarity (-1 to 1)
               - subjectivity: Subjectivity score (0 to 1)
    """
    words = word_tokenize(text.lower())

    cleaned_words = [word for word in words if word.isalnum() and word not in stop_words]

    pos_score = sum(1 for word in cleaned_words if word in positive_words)
    neg_score = sum(1 for word in cleaned_words if word in negative_words)

    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 0.000001)
    subjectivity = (pos_score + neg_score) / (len(cleaned_words) + 0.000001)

    return pos_score, neg_score, polarity, subjectivity

def calculate_readability(text):
    """
    Calculate readability metrics from text.

    Args:
        text (str): The text to analyze.

    Returns:
        tuple: (avg_sentence_length, percentage_complex_words, fog_index,
                avg_words_per_sentence, complex_word_count)
    """
    words = word_tokenize(text)
    sentences = sent_tokenize(text)

    avg_sentence_length = round(len(words) / len(sentences))
    complex_word_count = sum(1 for word in words if len(word) > 2 and word.isalnum() and word not in stop_words)
    percentage_complex_words = complex_word_count / len(words)

    fog_index = round(0.4 * (avg_sentence_length + percentage_complex_words), 4)
    avg_words_per_sentence = round(len(words) / len(sentences))

    return avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count

def calculate_syllable_per_word(text):
    """
    Calculate average syllables per word.

    Args:
        text (str): The text to analyze.

    Returns:
        float: Average syllables per word.
    """
    words = word_tokenize(text)
    total_syllables = 0

    for word in words:
        word = re.sub(r'[.,!?]', '', word)
        if len(word) > 2 and word.isalnum() and word not in stop_words:
            syllables = 0
            vowels = 'aeiouAEIOU'
            prev_char = None
            for char in word:
                if char in vowels and (prev_char is None or prev_char not in vowels):
                    syllables += 1
                prev_char = char
            if word.endswith('e'):
                syllables -= 1
            if syllables == 0:
                syllables = 1
            total_syllables += syllables

    avg_syllables_per_word = total_syllables / len(words)
    return avg_syllables_per_word

def calculate_personal_pronouns(text):
    """
    Count personal pronouns in the text.

    Args:
        text (str): The text to analyze.

    Returns:
        int: Count of personal pronouns (I, we, my, ours, us).
    """
    personal_pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text)
    return len(personal_pronouns)

def calculate_avg_word_length(text):
    """
    Calculate average word length in characters.

    Args:
        text (str): The text to analyze.

    Returns:
        float: Average word length.
    """
    words = word_tokenize(text)
    total_characters = sum(len(word) for word in words)
    avg_word_length = total_characters / len(words)
    return avg_word_length

def main():
    """
    Main function to process URLs from Excel, scrape, analyze, and save results.
    """
    excel_file = 'input.xlsx'
    df = pd.read_excel(excel_file)
    text_files_directory = 'extracted_text'
    os.makedirs(text_files_directory, exist_ok=True)

    for index, row in df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        text, headings = scrape_url(url.strip())

        if text:
            text_filename = os.path.join(text_files_directory, f'text_{url_id}.txt')
            with open(text_filename, 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            pos_score, neg_score, polarity, subjectivity = calculate_sentiment(text)
            avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count = calculate_readability(text)
            word_count = len(word_tokenize(text))
            syllable_per_word = calculate_syllable_per_word(text)
            personal_pronouns = calculate_personal_pronouns(text)
            avg_word_length = calculate_avg_word_length(text)

            df.at[index, 'POSITIVE SCORE'] = pos_score
            df.at[index, 'NEGATIVE SCORE'] = neg_score
            df.at[index, 'POLARITY SCORE'] = polarity
            df.at[index, 'SUBJECTIVITY SCORE'] = subjectivity
            df.at[index, 'AVG SENTENCE LENGTH'] = avg_sentence_length
            df.at[index, 'PERCENTAGE OF COMPLEX WORDS'] = percentage_complex_words
            df.at[index, 'FOG INDEX'] = fog_index
            df.at[index, 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_words_per_sentence
            df.at[index, 'COMPLEX WORD COUNT'] = complex_word_count
            df.at[index, 'WORD COUNT'] = word_count
            df.at[index, 'SYLLABLE PER WORD'] = syllable_per_word
            df.at[index, 'PERSONAL PRONOUNS'] = personal_pronouns
            df.at[index, 'AVG WORD LENGTH'] = round(avg_word_length, 4)

            print(f"Scores calculated and updated for URL ID {url_id}.")
            print(f"Extracted text saved to {text_filename}")

    output_file = 'output.xlsx'
    df.to_excel(output_file, index=False)
    print("Results saved to", output_file)

if __name__ == "__main__":
    main()