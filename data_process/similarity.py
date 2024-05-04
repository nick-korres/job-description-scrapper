from nltk.util import pairwise
from scipy.spatial.distance import cosine
import numpy as np
from scipy.sparse import csr_matrix
from joblib import Parallel, delayed 


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
    
    vec1_normalized = normalize_vector(vec1)
    vec2_normalized = normalize_vector(vec2)

    # # To get a measure of which word contributed what to the similarity 
    # weights = [a-b for a,b in zip(vec1_normalized,vec2_normalized)]
    # weights = np.array(weights)
    # top_indices = weights.argsort()[-10:][::-1]
    # top_weights = weights[top_indices]
    # list_of_vocab = list(vocab)
    # top_words = [[list_of_vocab[i],dist1.get(list_of_vocab[i]),dist2.get(list_of_vocab[i])] for i in top_indices]

    similarity = 1 - cosine(vec1_normalized, vec2_normalized)
    if similarity < lower_threshold:
        # For optimization reasons
        similarity = 0

    return similarity


def calculate_similarity_matrix(distribution_dict,n_jobs=-1):
    """
    Calculates the cosine similarity matrix for a list of word distributions.

    Args:
        distribution_dict (dict[str, nltk.FreqDist]): Dictionary of word distributions.

    Returns:
        numpy.ndarray: Cosine similarity matrix.
    """
    keys = list(distribution_dict.keys())
    n = len(keys)
    from math import sqrt
    k= Parallel(n_jobs=n_jobs)(delayed(sqrt)(i**2) for i in range(10))
    def calculate_pairwise_similarity(i, j):
         similarity_dict = {}
         similarity_dict["keys"] = [keys[i], keys[j]]
         print(f"Calculating similarity between {i} and {j}")
        #  similarity_dict["similarity"] = calculate_similarity(distribution_dict[keys[i]], distribution_dict[keys[j]])
         return similarity_dict
         
    
    similarity_list = Parallel(n_jobs=n_jobs)(delayed(calculate_pairwise_similarity)(i, j)for i in range(n) for j in range(i, n))


    return similarity_list