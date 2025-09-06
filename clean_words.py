# Remove words with more than 6 letters from words.txt
input_file = 'frequent_tolower.txt'
output_file = 'all_words.txt'
# You need a word frequency dictionary, e.g. from a CSV or JSON file
from wordfreq import zipf_frequency

with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
    for line in fin:
        word = line.strip()
        if zipf_frequency(word.lower(), 'en') > 3.0:
            fout.write(word + '\n')
