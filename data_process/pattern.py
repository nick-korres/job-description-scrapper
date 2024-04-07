from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy
from db.models.job_posts import find_jobs_where_search, job_post
from bs4 import BeautifulSoup
from nltk import FreqDist
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')


def sum_jobs_to_str(jobs:list[job_post]):
    job_strings = [job.description for job in jobs]
    combined_text = " ".join(job_strings)
    return combined_text


def find_frequent_words(html_string:str,top_number: int = 100):
    
    soup = BeautifulSoup(html_string, "html.parser")
    page_text = soup.get_text(separator=' ').lower()
    # Tokenize the text and extract common words
    tokens = word_tokenize(page_text)
    
    # Get English stop words
    stop_words = set(stopwords.words('english'))
    excluded = excluded_words
    [excluded.append(word) for word in stop_words]
    # Filter out non-word tokens and stop words
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in excluded]

    # Count frequency of filtered tokens
    word_freq = Counter(filtered_tokens)
    # Pattern Recognition (Identify common skills, keywords, etc.)
    common_keywords = [] 
    [common_keywords.append({word : freq })  for word, freq in word_freq.most_common(top_number)]# Example: Extract top 10 common words

    # TODO Recommendation Engine (Using common_keywords to find similar job descriptions)

    return common_keywords


def find_top_words(jobs:list[job_post]):
    combined_text = sum_jobs_to_str(jobs)
    top_words = find_frequent_words(combined_text)
    return top_words


excluded_words = [
    'skills','experience','team','premium','work','development','software','data','set','job','type','see','working','alert','jobs','add','stand','applicant','greece','knowledge'
    ]




def get_word_distribution(jobs_to_analyze: list[job_post],excluded_words=excluded_words ):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    
    distribution_dict :dict[str,FreqDist]= {}
    for job in jobs_to_analyze:
        soup = BeautifulSoup(job.description, "html.parser")
        page_text = soup.get_text(separator=' ').lower()
        tokens = word_tokenize(page_text)
        filtered_tokens = [word for word in tokens if word.isalpha() and word.casefold() not in all_excluded_words]

        dist = FreqDist(filtered_tokens)
        distribution_dict[job.linkedin_id] = dist

    return distribution_dict

        





