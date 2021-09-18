#%%
import pandas as pd
import re

freqxml_pdf = pd.read_csv('freq.xml', names=['word'])
freqxml_values = freqxml_pdf['word'].values

freq_dict = {}
for value in freqxml_values:
    pair = re.findall(r'f\=\"(\d+)\".+?>(\w+)<', value)
    if pair == []:
        continue
    freq = pair[0][0]
    word = pair[0][1]
    freq_dict[word] = freq

for value in freqxml_values:
    pair = re.findall(r'f\=\"(\d+)\".+?>(\w+)<', value)
    if pair == []:
        continue
    freq = pair[0][0]
    word = pair[0][1]
    freq_dict[word.capitalize()] = freq

freq_df = pd.DataFrame(list(freq_dict.keys()), columns=['word'])

freq_df[freq_df['word'] == 'De']
# %%
