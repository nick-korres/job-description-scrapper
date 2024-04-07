from matplotlib import pyplot as plt
import numpy
from db.models.job_posts import find_jobs_where_search, job_post
from data_process.pattern import get_word_distribution
from nltk import FreqDist

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
    plt.show()


jobs_to_analyze : list[job_post]  = find_jobs_where_search(None)
distribution_dict :dict[str,FreqDist]  = get_word_distribution(jobs_to_analyze,excluded_words=[])
# id = jobs_to_analyze[0].linkedin_id
# title = jobs_to_analyze[0].title
# company = jobs_to_analyze[0].name
# plot_word_distribution(distribution_dict[id],title=f'{title} at {company} Word Distribution')
freq_dists :list[FreqDist] = list(distribution_dict.values())
combined_freq_dist = FreqDist()
for freq_dist in freq_dists:
    combined_freq_dist += freq_dist

sorted_freq_dist = sorted(combined_freq_dist.items(), key=lambda item: item[1], reverse=True)
sorted_freq_dist = FreqDist(dict(sorted_freq_dist))
plot_word_distribution(sorted_freq_dist,title="Word Distribution for all jobs")

