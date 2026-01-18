# Quantitative Sentiment Mapping of Web-Based Essays

## Overview

This project is a comprehensive **Web Scraping and Sentiment Analysis Tool** designed to automate the extraction, analysis, and quantification of textual content from web-based essays and articles. By processing URLs provided in an Excel spreadsheet (input.xlsx), the tool scrapes relevant text, performs advanced sentiment analysis using curated dictionaries, and calculates various readability and linguistic metrics to provide quantitative insights into the emotional tone, complexity, and structural characteristics of the content.

### What This Project Does

The core functionality revolves around transforming qualitative web content into quantitative data through a multi-step pipeline:

1. **Web Scraping**: Extracts clean, structured text from specified URLs, focusing on paragraph content and headings while filtering out irrelevant elements like headers, footers, images, and media.

2. **Sentiment Analysis**: Leverages a robust dictionary-based approach with **2,006 positive words** and **4,783 negative words** to compute sentiment scores, polarity, and subjectivity metrics.

3. **Readability Assessment**: Calculates multiple readability indices including Fog Index, average sentence length, and complex word percentages to evaluate text complexity.

4. **Linguistic Metrics**: Provides comprehensive word-level statistics such as syllable counts, personal pronoun usage, and average word lengths.

5. **Stop Word Filtering**: Utilizes a comprehensive stop word list of **14,104 words** across multiple categories (auditor, currencies, dates, generic, geographic, names) to ensure accurate analysis by removing noise.

### Key Numerical Statistics and Metrics

The tool generates **14 quantitative metrics** for each processed URL:

- **Sentiment Metrics**:
  - Positive Score: Count of positive words (range: 0 to several hundred depending on text length)
  - Negative Score: Count of negative words (range: 0 to several hundred)
  - Polarity Score: Normalized sentiment polarity (-1 to +1, where -1 is most negative, +1 is most positive)
  - Subjectivity Score: Measure of opinionated content (0 to 1, where 0 is objective, 1 is subjective)

- **Readability Metrics**:
  - Average Sentence Length: Words per sentence (typically 15-30 for standard English text)
  - Percentage of Complex Words: Proportion of words with >2 syllables (usually 10-20% in readable text)
  - Fog Index: Readability score (lower values indicate easier reading, typically 8-15 for general audience)
  - Average Words per Sentence: Redundant with sentence length but provided for compatibility

- **Word-Level Statistics**:
  - Complex Word Count: Number of words with >2 syllables
  - Word Count: Total words in the extracted text
  - Syllable per Word: Average syllables per word (typically 1.2-1.8 in English)
  - Personal Pronouns: Count of first-person pronouns (I, we, my, ours, us)
  - Average Word Length: Characters per word (typically 4-6 in English)

These metrics enable quantitative comparison across multiple essays, supporting applications in content analysis, academic research, market sentiment tracking, and automated content evaluation.

## Features

- **Automated Web Scraping**: Handles multiple URLs concurrently with error resilience
- **Dictionary-Based Sentiment Analysis**: Uses industry-standard positive/negative word lists
- **Comprehensive Readability Calculations**: Multiple indices for thorough text analysis
- **Stop Word Management**: Extensive stop word filtering across multiple domains
- **Excel Integration**: Reads input from Excel files and writes results back
- **Text Preservation**: Saves extracted text for manual review and verification
- **Robust Error Handling**: Graceful handling of network failures and parsing errors

## Prerequisites

- **Python Version**: 3.7 or higher
- **Operating System**: macOS, Windows, or Linux
- **Dependencies**: Listed in `requirements.txt`
- **Input File**: `input.xlsx` with columns 'URL_ID' and 'URL'

## Installation and Initialization

### 1. Clone or Download the Project

Ensure you have the project files in a local directory:

```
Quantitative-Sentiment-Mapping-of-Web-Based-Essays/
├── Web_Scraping_and_Sentiment_Analysis.py
├── requirements.txt
├── MasterDictionary/
│   ├── positive-words.txt
│   └── negative-words.txt
└── StopWords/
    ├── StopWords_Auditor.txt
    ├── StopWords_Currencies.txt
    ├── StopWords_DatesandNumbers.txt
    ├── StopWords_Generic.txt
    ├── StopWords_GenericLong.txt
    ├── StopWords_Geographic.txt
    └── StopWords_Names.txt
```

### 2. Set Up Python Environment

Create a virtual environment (recommended):

```bash
python -m venv sentiment_env
source sentiment_env/bin/activate  # On Windows: sentiment_env\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `requests`: For HTTP requests to scrape web content
- `beautifulsoup4`: For HTML parsing and text extraction
- `pandas`: For Excel file handling and data manipulation
- `nltk`: For natural language processing tasks

### 4. Download NLTK Data

The script automatically downloads required NLTK data on first run, but you can pre-download it:

```python
import nltk
nltk.download('punkt_tab')
```

### 5. Prepare Input File

Create `input.xlsx` with the following structure:

| URL_ID | URL                          |
|--------|------------------------------|
| 1      | https://example.com/essay1   |
| 2      | https://example.com/essay2   |
| ...    | ...                          |

- **URL_ID**: Unique identifier for each URL (integer or string)
- **URL**: Full URL to the webpage containing the essay/article

## Execution

### Running the Script

Execute the main script from the project directory:

```bash
python Web_Scraping_and_Sentiment_Analysis.py
```

### What Happens During Execution

1. **Loading Dictionaries**: The script loads positive words, negative words, and stop words from their respective files.

2. **Reading Input**: Parses `input.xlsx` to extract URL_ID and URL pairs.

3. **Web Scraping**: For each URL:
   - Sends HTTP GET request
   - Parses HTML content using BeautifulSoup
   - Extracts paragraph text and headings
   - Filters out unwanted elements

4. **Text Analysis**: For each extracted text:
   - Tokenizes words and sentences
   - Calculates sentiment scores
   - Computes readability metrics
   - Counts linguistic features

5. **Saving Results**: 
   - Writes extracted text to `extracted_text/text_{URL_ID}.txt`
   - Updates the DataFrame with calculated metrics
   - Saves results to `output.xlsx`

6. **Progress Reporting**: Prints status messages for each processed URL.

### Expected Output

- **`output.xlsx`**: Original input columns plus 14 new metric columns
- **`extracted_text/`**: Directory containing individual text files for each URL
- **Console Output**: Progress messages and completion confirmation

## Basic Error Handling

The script includes several error handling mechanisms:

### Network Errors
- **HTTP Failures**: If a URL returns non-200 status code, the script logs the failure and skips that URL
- **Connection Timeouts**: Uses default request timeouts; consider adding custom timeout handling for slow connections
- **Invalid URLs**: Malformed URLs will cause request exceptions, handled gracefully

### File System Errors
- **Missing Input File**: `pandas.read_excel()` will raise `FileNotFoundError` if `input.xlsx` doesn't exist
- **Permission Issues**: Writing to `output.xlsx` or `extracted_text/` may fail if permissions are insufficient
- **Encoding Issues**: Dictionary files use ISO-8859-1 encoding; ensure your system supports this

### Data Processing Errors
- **Empty Text**: URLs with no extractable text will have zero values for all metrics
- **NLTK Tokenization**: Requires internet connection for initial data download
- **Division by Zero**: Protected by adding small epsilon values (0.000001) in calculations

### Common Issues and Solutions

1. **"Failed to fetch URL"**: Check URL validity and internet connection
2. **"No module named 'requests'"**: Ensure dependencies are installed via `pip install -r requirements.txt`
3. **"FileNotFoundError"**: Verify all required files and directories exist
4. **Empty results**: Check if target websites have changed their structure or blocked scraping

### Debugging Tips

- Run with a small input file (1-2 URLs) first to test functionality
- Check `extracted_text/` files to verify text extraction quality
- Monitor console output for specific error messages
- Ensure Python environment has necessary permissions for file operations

## Project Structure

```
Quantitative-Sentiment-Mapping-of-Web-Based-Essays/
├── Web_Scraping_and_Sentiment_Analysis.py  # Main script
├── requirements.txt                        # Python dependencies
├── README.md                               # This file
├── input.xlsx                              # Input file (user provided)
├── output.xlsx                             # Output file (generated)
├── extracted_text/                         # Directory for extracted texts (generated)
│   ├── text_1.txt
│   ├── text_2.txt
│   └── ...
├── MasterDictionary/                       # Sentiment dictionaries
│   ├── positive-words.txt                  # 2,006 positive words
│   └── negative-words.txt                  # 4,783 negative words
└── StopWords/                              # Stop word lists
    ├── StopWords_Auditor.txt
    ├── StopWords_Currencies.txt
    ├── StopWords_DatesandNumbers.txt
    ├── StopWords_Generic.txt
    ├── StopWords_GenericLong.txt
    ├── StopWords_Geographic.txt
    └── StopWords_Names.txt                 # Total: 14,104 stop words
```

## Limitations and Considerations

- **Web Scraping Ethics**: Respect website terms of service and robots.txt
- **Dynamic Content**: May not capture JavaScript-rendered content
- **Language Support**: Optimized for English text analysis
- **Dictionary Coverage**: Sentiment analysis limited to provided word lists
- **Performance**: Processing time scales with number of URLs and text length

## Future Prospects

This project has significant potential for expansion and enhancement in several key areas:

### Enhanced Web Scraping Capabilities
- **JavaScript Rendering Support**: Integration with headless browsers (e.g., Selenium, Playwright) to handle dynamic content and single-page applications
- **API Integration**: Support for scraping content from REST APIs and GraphQL endpoints
- **Rate Limiting and Proxy Management**: Built-in mechanisms to handle large-scale scraping with respect to website policies

### Advanced Sentiment Analysis
- **Machine Learning Models**: Incorporation of transformer-based models (BERT, RoBERTa) for more nuanced sentiment detection
- **Multi-language Support**: Expansion to support sentiment analysis in multiple languages with appropriate dictionaries
- **Context-Aware Analysis**: Implementation of contextual sentiment analysis considering word relationships and negations

### Expanded Metrics and Analytics
- **Additional Readability Indices**: Integration of more sophisticated readability formulas (e.g., Flesch-Kincaid, SMOG Index)
- **Semantic Analysis**: Addition of topic modeling and keyword extraction using techniques like TF-IDF or LDA
- **Comparative Analytics**: Built-in visualization and comparison tools for analyzing trends across multiple documents

### Performance and Scalability Improvements
- **Parallel Processing**: Multi-threading or distributed processing for handling large numbers of URLs efficiently
- **Caching Mechanisms**: Implementation of intelligent caching to avoid re-processing unchanged content
- **Cloud Integration**: Deployment options for cloud platforms (AWS, GCP, Azure) with serverless functions

### User Interface and Accessibility
- **Web Dashboard**: Development of a web-based interface for easier input management and result visualization
- **API Endpoints**: Creation of RESTful APIs for integration with other applications and workflows
- **Export Options**: Support for additional output formats (JSON, CSV, database integration)

### Research and Academic Applications
- **Citation Analysis**: Integration with academic databases for automated literature review and citation sentiment analysis
- **Longitudinal Studies**: Features for tracking sentiment changes over time across the same URLs
- **Collaborative Features**: Multi-user support for team-based content analysis projects

The project roadmap prioritizes maintaining the current dictionary-based approach while gradually incorporating modern NLP techniques to enhance accuracy and expand capabilities. Community contributions and feedback will play a crucial role in shaping these future developments.

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is provided as-is for educational and research purposes. Please ensure compliance with applicable laws and website terms of service when scraping content.

## Support

For issues or questions:
1. Check the error handling section above
2. Verify all prerequisites are met
3. Test with a minimal input file
4. Review console output for specific error messages