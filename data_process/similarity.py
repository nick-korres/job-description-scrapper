import concurrent.futures
import math
from typing import Dict, List, Literal, TypedDict
from nltk.util import pairwise
from scipy.spatial.distance import cosine
import numpy as np
from scipy.sparse import csr_matrix
from joblib import Parallel, delayed 
from nltk import FreqDist
from scipy.special import kl_div




def list_to_matrix(similarity_list, key_map : list[str]):
    """
    Converts a list of similarity dictionaries to a similarity matrix.

    Args:
        similarity_list (list[dict]): List of similarity dictionaries.
        n (int): Number of unique keys in the similarity dictionary.

    Returns:
        numpy.ndarray: Similarity matrix.
    """
    # Initialize an empty matrix
    n = len(key_map)
    similarity_matrix = np.zeros((n, n))

    for similarity_dict in similarity_list:
        keys = similarity_dict["keys"]
        similarity = similarity_dict["similarity"]
        i = key_map.index(keys[0]) 
        j = key_map.index(keys[1])
        similarity_matrix[i, j] = similarity
        similarity_matrix[j, i] = similarity

    return similarity_matrix

def get_n_highest(similarity_matrix, keys, n):
    """
    Gets the n highest values in a matrix along with their corresponding keys as a dictionary.

    Args:
        similarity_matrix (numpy.ndarray): The input similarity matrix.
        keys (list): A list of keys (labels) for each row/column in the matrix.
        n (int): The number of highest values to retrieve.

    Returns:
        dict: A dictionary where keys are from the 'keys' list and values are the n highest values.
    """

    # Flatten the matrix for efficient sorting
    # flat_matrix = similarity_matrix.flatten()
    flat_matrix = np.asarray(similarity_matrix.todense()).flatten()

    # Sort indices in descending order and get the top n
    sorted_indices = np.argsort(flat_matrix)[::-1][:n]

    #   # Extract highest values based on sorted indices
    #   highest_values = flat_matrix[sorted_indices]

    # Reshape the flattened indices into a 2D array for efficient key retrieval
    row_cols = np.unravel_index(sorted_indices, similarity_matrix.shape)

    # Create a dictionary with keys and corresponding highest values
    # row_cols[1][0] , row_cols[1][1] are the indices of the highest value
    # similarity_matrix[ row_cols[1][0] , row_cols[1][1] ] = flat_matrix[ sorted_indices[0] ]
    highest_values = []
    for i in range(n):
        original_row = row_cols[0][i]
        original_col = row_cols[1][i]
        current_value_keys = [keys[original_row], keys[original_col]]
        similarity = similarity_matrix[original_row, original_col]
        highest_values.append({"keys": current_value_keys, "similarity": similarity})

    return highest_values

def normalize_vector(vec):
  """
  Normalizes a vector to unit length (l2-norm).

  Args:
      vec (list): List of word counts.

  Returns:
      list: Normalized vector.
  """
  norm = np.linalg.norm(vec)  # Calculate vector magnitude
  return [v / norm if norm != 0 else 0 for v in vec]  # Divide each element by norm


def calculate_similarity_kl_div(dist1, dist2):
    """
    Calculate Kullback-Leibler (KL) Divergence between two distributions represented as dictionaries of term frequencies.
    
    Parameters:
        dist1 (dict): First distribution.
        dist2 (dict): Second distribution.
        
    Returns:
        float: KL Divergence between the two distributions.
    """
    # Combine keys from both distributions
    all_terms = set(dist1.keys()) | set(dist2.keys())
    
    # Convert distributions to numpy arrays
    dist1_array = np.array([dist1.get(term, 0) for term in all_terms])
    dist2_array = np.array([dist2.get(term, 0) for term in all_terms])
    
    # Normalize distributions to probabilities
    dist1_prob = dist1_array / dist1_array.sum()
    dist2_prob = dist2_array / dist2_array.sum()
    
    # Calculate KL Divergence
    kl_divergence_value = kl_div(dist1_prob, dist2_prob).sum()
    
    return kl_divergence_value

def word_weights_idf(dist1 :FreqDist, dist2:FreqDist):
    """
    This function takes two FreqDist objects and calculates a list of weights for each word.

    Args:
        fdist1 (FreqDist): A FreqDist object containing the distribution of words in the first job description.
        fdist2 (FreqDist): A FreqDist object containing the distribution of words in the second job description.

    Returns:
        list: A list of weights for each word, where the weight is inversely correlated to its frequency.
    """
    total_words = sum(dist1.values()) + sum(dist2.values())

    combined_dist = FreqDist(dist1)
    combined_dist.update(dist2)

    


    idf_weights = { term: np.log(abs(total_words) / (abs(df) + 1)) for term, df in combined_dist.items()}
    # most_common = combined_dist.most_common(5)
    # most_common_weights = {term: idf_weights[term] for term, df in most_common}
    # least_common = combined_dist.most_common()[:-5:-1]
    # least_common_weights = {term: idf_weights[term] for term, df in least_common}
    for term,value in idf_weights.items():    
        if value < 0:
            idf_weights[term] = 0

    return idf_weights


def calculate_similarity(dist1, dist2,lower_threshold = 0.0):
    """
    Calculates the cosine similarity between two word distributions.

    Args:
        dist1 (nltk.FreqDist): First word distribution.
        dist2 (nltk.FreqDist): Second word distribution.

    Returns:
        float: Cosine similarity between the two distributions.
    """
    # Combine vocabularies (to handle potential missing words in one distribution)
    vocab = set(dist1.keys()) | set(dist2.keys())
    
    # Count for each word in the vocabulary
    # Keep them in same order   
    vec1 = [dist1.get(w, 0) for w in vocab]  
    vec2 = [dist2.get(w, 0) for w in vocab]

    weights = word_weights_idf(dist1,dist2)
    weights = [weights[w] for w in vocab]
    
    vec1_normalized = normalize_vector(vec1)
    vec2_normalized = normalize_vector(vec2)

    if np.all(vec1_normalized == 0) or np.all(vec2_normalized == 0):
        similarity = 0  
    else:
        similarity = 1 - cosine(vec1_normalized, vec2_normalized,weights)
    # limit to 3 decimals
    similarity = round(similarity, 3)
    if np.isnan(similarity):
        # print("NAN detected in similarity calculation")
        similarity = 0

    # if similarity < lower_threshold:
    #     # For optimization reasons
    #     similarity = 0

    return similarity

ComparableFields = Literal["title", "description", "name", "sector", "location","remote","skills_required"]
class AllFieldsDist(TypedDict):
    title: FreqDist
    description: FreqDist
    name: FreqDist
    sector: FreqDist
    location: FreqDist
    remote: FreqDist
    skills_required: FreqDist
class AllFieldsWeights(TypedDict):
    title: int
    description: int
    name: int
    sector: int
    location: int
    remote: int
    skills_required: int

def calculate_similarity_all_fields(dist1: AllFieldsDist , dist2 : AllFieldsDist, weights : AllFieldsWeights ,lower_threshold = 0.0):
    total_weight = sum(weights.values())
    threshold = 1e-10 
    # because of floating point precision , sometimes the sum is not exactly 1
    if abs(total_weight - 1) > threshold:
        raise ValueError(f"Weights should sum to 1 but they sum to {total_weight}")
    similarity: float = 0
    for field in weights :

        # if weights[field] > threshold : continue

        if field not in dist1:
            dist1[field] = FreqDist()        

        if field not in dist2:
            dist2[field] = FreqDist()
            
        field_similarity = calculate_similarity(dist1[field],dist2[field],lower_threshold)
        similarity += weights[field]*field_similarity
        # print(f"Similarity for {field} is {field_similarity}")
    return similarity

def fill_dict(dist1,id,weights,lower_threshold ,id_to_dist):
    dist2 = id_to_dist[id]
    sim = calculate_similarity_all_fields(dist1,dist2,weights,lower_threshold)
    return  { id : sim }

def calculate_similarity_all_fields_parallel(dist1: AllFieldsDist , id_to_dist : Dict[str,AllFieldsDist], weights : AllFieldsWeights ,lower_threshold = 0.0):
    results = []
    max_workers = 10


    input_list = [(dist1, key, weights, lower_threshold) for key,_ in id_to_dist.items()]

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fill_dict, *obj,id_to_dist) for obj in input_list]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    collective_results = {key:value for result in results for key,value in result.items()}
    return collective_results


# def calculate_similarity_matrix(distribution_dict,n_jobs=-1):
#     """
#     Calculates the cosine similarity matrix for a list of word distributions.

#     Args:
#         distribution_dict (dict[str, nltk.FreqDist]): Dictionary of word distributions.

#     Returns:
#         numpy.ndarray: Cosine similarity matrix.
#     """
#     keys = list(distribution_dict.keys())
#     n = len(keys)
#     from math import sqrt
#     k= Parallel(n_jobs=n_jobs)(delayed(sqrt)(i**2) for i in range(10))
#     def calculate_pairwise_similarity(i, j):
#          similarity_dict = {}
#          similarity_dict["keys"] = [keys[i], keys[j]]
#          print(f"Calculating similarity between {i} and {j}")
#         #  similarity_dict["similarity"] = calculate_similarity(distribution_dict[keys[i]], distribution_dict[keys[j]])
#          return similarity_dict
         
    
#     similarity_list = Parallel(n_jobs=n_jobs)(delayed(calculate_pairwise_similarity)(i, j)for i in range(n) for j in range(i, n))


#     return similarity_list

