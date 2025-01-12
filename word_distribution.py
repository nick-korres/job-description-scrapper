import time
from matplotlib import pyplot as plt
import numpy
from db.models.job_posts import find_jobs_where_search, job_post
from data_process.pattern import  get_word_distribution_union

from utils.files.json_cache import save_json


def plot_word_distribution(distribution_dict,num_of_top_words=20,title:str="Word Distribution"):
    labels, values = zip(*distribution_dict.items())
    if len(labels) < num_of_top_words:
        num_of_top_words = len(labels)
    most_common_labels: list[str] = labels[:num_of_top_words]
    most_common_values : list[int] = values[:num_of_top_words]
    others_value = sum(values[num_of_top_words:]) 
    plt.text(1, 1, f'other words : {others_value}', fontsize=12)

    def absolute_value(val):
        a  = numpy.round(val/100.*numpy.array(most_common_values).sum(), 0)
        return int(a)
    plt.title(title)
    plt.pie(most_common_values, labels=most_common_labels,autopct=absolute_value,)
    plt.show(block=True)

def plot_double_word_distribution(distribution_dict1,distribution_dict2,num_of_top_words=20,title:str="Word Distribution"):
    labels1, values1 = zip(*distribution_dict1.items())
    labels2, values2 = zip(*distribution_dict2.items())
    if len(labels1) < num_of_top_words:
        num_of_top_words = len(labels1)
    most_common_labels1: list[str] = labels1[:num_of_top_words]
    most_common_values1 : list[int] = values1[:num_of_top_words]
    most_common_labels2: list[str] = labels2[:num_of_top_words]
    most_common_values2 : list[int] = values2[:num_of_top_words]
    others_value1 = sum(values1[num_of_top_words:]) 
    others_value2 = sum(values2[num_of_top_words:]) 


    def absolute_value(val):
        a  = numpy.round(val/100.*numpy.array(most_common_values1).sum(), 0)
        return int(a)

    fig, axs = plt.subplots(1, 2)
    fig.suptitle(title)
    axs[0].pie(most_common_values1, labels=most_common_labels1,autopct=absolute_value,)
    axs[0].text(1, 1, f'other words : {others_value1}', fontsize=12)
    axs[1].pie(most_common_values2, labels=most_common_labels2,autopct=absolute_value,)
    axs[1].text(1, 1, f'other words : {others_value2}', fontsize=12)
 
    plt.show(block=True)

def plot_similarity_heatmap(similarity_matrix):
  """
  Plots a heatmap of the similarity matrix.

  Args:
      similarity_matrix (numpy.ndarray): The input similarity matrix.
  """

  # Create a new figure for the heatmap
  plt.figure(figsize=(10, 6))  # Adjust figure size as needed

  # Create the heatmap using pcolor
  heatmap = plt.pcolor(similarity_matrix, cmap="YlGnBu")  # Adjust cmap for color scheme

  # Add colorbar for interpretation
  plt.colorbar(heatmap, label="Similarity Score")

  # Set labels for axes (optional)
  plt.xlabel("Document Index")
  plt.ylabel("Document Index")

  # Set ticks for axes (optional)
  if len(similarity_matrix) <= 20:  # Adjust limit based on matrix size
    plt.xticks(numpy.arange(len(similarity_matrix)))
    plt.yticks(numpy.arange(len(similarity_matrix)))

  # Add labels for each cell (optional)
  # plt.text(..., ..., str(value), ha='center', va='center', fontsize=8)  # Uncomment for cell labels

  # Set title for the heatmap
  plt.title("Similarity Heatmap")

  # Display the heatmap
  plt.show()    

search = "test_filter"

jobs_to_analyze : list[job_post]  = find_jobs_where_search(search)
jobs_to_analyze = jobs_to_analyze[:100]
# before  = time.time()
# # distribution_dict1 = get_word_distribution_multithread(input=jobs_to_analyze,excluded_words=[],max_threads=10)
# distribution_dict2 = get_word_distribution(jobs_to_analyze,excluded_words=[])
# after = time.time()
# print(f"Multi thread took {after-before} seconds")
before  = time.time()
# distribution_dict: dict[str,FreqDist] = get_word_distributions(jobs_to_analyze,excluded_words=[])
distribution_union = get_word_distribution_union(jobs_to_analyze,excluded_words=[])
after = time.time()
print(f"Single thread took {after-before} seconds")
# id = jobs_to_analyze[0].linkedin_id
# title = jobs_to_analyze[0].title
# company = jobs_to_analyze[0].name
# plot_word_distribution(distribution_dict[id],title=f'{title} at {company} Word Distribution')
save_json("distribution_union.json",distribution_union)

# freq_dists :list[FreqDist] = list(distribution_dict.values())
# combined_freq_dist = FreqDist()
# for freq_dist in freq_dists:
#     combined_freq_dist += freq_dist

# sorted_freq_dist = sorted(combined_freq_dist.items(), key=lambda item: item[1], reverse=True)
# sorted_freq_dist = FreqDist(dict(sorted_freq_dist))

# # It is a symmetric matrix so we export the upper triangle as a list
# sim_list = calculate_similarity_matrix(distribution_dict,20)

# # key_map = [job.linkedin_id for job in jobs_to_analyze]
# # matrix = list_to_matrix(sim_list,key_map)
# # plot_similarity_heatmap(matrix)

# sim_list = [sim for sim in sim_list if sim["keys"][0] != sim["keys"][1] ]
# most_similar = sorted(sim_list, key=lambda item: item["similarity"],reverse=True)[:10]

# for sim in most_similar:
#     key1 = sim["keys"][0]
#     key2 = sim["keys"][1]
#     name1 = [job.title for job in jobs_to_analyze if job.linkedin_id == key1][0]
#     name2 = [job.title for job in jobs_to_analyze if job.linkedin_id == key2][0]
#     sim.update({"names":[name1,name2],"similarity":sim["similarity"]})

# # plot_word_distribution(sorted_freq_dist,title="Word Distribution for all jobs")
# for sim in most_similar:
#     title = f'{sim["names"][0]} and {sim["names"][1]} Word Distribution \n             similarity : {sim["similarity"]}'
#     dist1 = distribution_dict[sim["keys"][0]]
#     dist2 = distribution_dict[sim["keys"][1]] 
#     plot_double_word_distribution(dist1,dist2,num_of_top_words=10,title=title)
