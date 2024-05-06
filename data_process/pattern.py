from collections import Counter
from enum import Enum
import threading
from typing import TypedDict
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from data_process.similarity import AllFieldsDist, ComparableFields
from db.models.job_posts import find_jobs_where_search, job_post
from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.stem import PorterStemmer
import string
from nltk.stem import WordNetLemmatizer
from joblib import Parallel, delayed 

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


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




def get_word_distributions(jobs_to_analyze: list[job_post],excluded_words=excluded_words ):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    lemmatizer = WordNetLemmatizer()
    # stemmer = PorterStemmer()
    distribution_dict :dict[str,FreqDist]= {}
    for job in jobs_to_analyze:
        soup = BeautifulSoup(job.description, "html.parser")
        page_text = soup.get_text(separator=' ').lower()
        tokens = word_tokenize(page_text)
        filtered_tokens = [word for word in tokens if word.isalpha() and word.casefold() not in all_excluded_words]
        
        # filtered_tokens = [stemmer.stem(word) for word in filtered_tokens]
        filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]

        
        filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        filtered_tokens = [word for word in filtered_tokens if len(word) > 2]

        dist = FreqDist(filtered_tokens)
        distribution_dict[job.linkedin_id] = dist

    return distribution_dict

def get_word_distribution_union(jobs_to_analyze: list[job_post],excluded_words=excluded_words,freq_threshold=None):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()
    combined_text = ""
    for job in jobs_to_analyze:
        combined_text += job.description
    
    soup = BeautifulSoup(combined_text, "html.parser")
    page_text = soup.get_text(separator=' ').lower()
    tokens = word_tokenize(page_text)
    filtered_tokens = [word for word in tokens if word.isalpha() and word.casefold() not in all_excluded_words]
    
    # filtered_tokens = [stemmer.stem(word) for word in filtered_tokens]

    filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]

    filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    filtered_tokens = [word for word in filtered_tokens if len(word) > 2]

    dist = FreqDist(filtered_tokens)

    if freq_threshold:
        dist = {k:v for k,v in dist.items() if v > freq_threshold}
        
    return dist
        
def get_word_distribution_all_fields_union(jobs_to_analyze: list[job_post],excluded_words=excluded_words,freq_threshold=None):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    lemmatizer = WordNetLemmatizer()

    comparable_fields = [field for field in ComparableFields.__args__]

    combined_text_dict = { field: "" for field in comparable_fields}

    for job in jobs_to_analyze:
        for field in comparable_fields:
            combined_text_dict[field] += getattr(job,field)
    
    dist_dict : AllFieldsDist = {}
    for field in comparable_fields:
        soup = BeautifulSoup(combined_text_dict[field], "html.parser")
        page_text = soup.get_text(separator=' ').lower()
        tokens = word_tokenize(page_text)
        filtered_tokens = [word for word in tokens if word.isalpha() and word.casefold() not in all_excluded_words]
    
        filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]

        filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

        filtered_tokens = [word for word in filtered_tokens if len(word) > 2]

        dist = FreqDist(filtered_tokens)
        if freq_threshold:
            dist = {k:v for k,v in dist.items() if v > freq_threshold}
        dist_dict[field] = dist

    return dist_dict
    
    

def parse_job_description(job:job_post,all_excluded_words=[]):
        soup = BeautifulSoup(job.description, "html.parser")
        page_text = soup.get_text(separator=' ').lower()
        tokens = word_tokenize(page_text)
        filtered_tokens = [word for word in tokens if word.isalpha() and word.casefold() not in all_excluded_words]
        # stemmer = PorterStemmer()
        # filtered_tokens = [stemmer.stem(word) for word in filtered_tokens]
        filtered_tokens = [word for word in filtered_tokens if word not in string.punctuation]

        # lemmatizer = WordNetLemmatizer()
        # filtered_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
        # filtered_tokens = [word for word in filtered_tokens if len(word) > 2]

        dist = FreqDist(filtered_tokens)
        return dist

def get_word_distribution_parallel(jobs_to_analyze: list[job_post],excluded_words=excluded_words,n_jobs=-1):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    
    distribution_dict :dict[str,FreqDist]= {}
    test_dict = {}
    def fill_distribution_dict(job,all_excluded_words,distribution_dict):
        dist = parse_job_description(job,all_excluded_words)
        distribution_dict[job.linkedin_id] = dist
        test_dict[job.linkedin_id] = dist
        return distribution_dict


    result = Parallel(n_jobs=n_jobs)(delayed(fill_distribution_dict)(job,all_excluded_words,distribution_dict) for job in jobs_to_analyze)
    distribution_dict = {k: v for d in result for k, v in d.items()}

    return distribution_dict

def get_word_distribution_multithreaded(jobs_to_analyze: list[job_post],excluded_words=excluded_words,max_threads=20):
    stop_words = set(stopwords.words('english'))
    all_excluded_words = excluded_words + list(stop_words)
    
    distribution_dict :dict[str,FreqDist]= {}
    test_dict = {}
    def fill_distribution_dict(job_list:list[job_post],all_excluded_words,distribution_dict):
        for job in job_list:
            dist = parse_job_description(job,all_excluded_words)
            distribution_dict[job.linkedin_id] = dist
            test_dict[job.linkedin_id] = dist
            return distribution_dict
    
    chunk_size = max(len(jobs_to_analyze) // max_threads, 1)
    job_chunks = [jobs_to_analyze[i:i+chunk_size] for i in range(0, len(jobs_to_analyze), chunk_size)]
    threads = []
    for i, jobs in enumerate(job_chunks):
        thread = threading.Thread(target=fill_distribution_dict, args=(jobs[i % max_threads],all_excluded_words,distribution_dict))
        threads.append(thread)

    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    return distribution_dict

class InputType(Enum):
    LIST = "list"
    DICT = "dict"

class MultiSettings(TypedDict):
    max_threads: int
    input_type: InputType
    aggregate_type: InputType


def multithread_wrapper(settings:MultiSettings=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            

            list_to_multithread = kwargs.get("input",None)
            if list_to_multithread is None:
                raise ValueError(f" input must be specified")
            
            max_threads = kwargs.get("max_threads",None)
            if max_threads is None:
                max_threads = settings.get("max_threads",None)
            if max_threads is None:
                raise ValueError("max_threads must be specified")
            

            aggregate_type = settings.get("aggregate_type",None)
            if aggregate_type == InputType.LIST.value:
                results = []
            elif aggregate_type == InputType.DICT.value:
                results = {}
            else:
                raise ValueError(f"aggregate_type must be either {InputType.LIST} or {InputType.DICT}")
            
            


            function_args_kw = kwargs.get("extra_args",{})

            chunk_size = max(len(list_to_multithread) // max_threads, 1)
            work_chunks = [list_to_multithread[i:i+chunk_size] for i in range(0, len(list_to_multithread), chunk_size)]
            threads = []
            for i, works in enumerate(work_chunks):
                thread = threading.Thread(target=func,args=(work_chunks[i % max_threads],results,), kwargs=function_args_kw )
                threads.append(thread)

            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()

            return results
        return wrapper
    return decorator

default_settings = {
    "max_threads":4,
    "input_type":InputType.LIST.value,
    "aggregate_type":InputType.DICT.value
}

@multithread_wrapper(settings=default_settings)
def get_word_distribution_multithread(input:list[job_post],results=[],extra_args= {"excluded_words":[]},settings:MultiSettings={}):
    excluded_words = extra_args.get("excluded_words",[])
    for job in input:
        try:
            dist = parse_job_description(job,excluded_words)
            results[job.linkedin_id] = dist

        except Exception as e:
            print(f"Error processing job {job.linkedin_id}")
            print(e)
            continue