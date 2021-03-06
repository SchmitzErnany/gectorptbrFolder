#%%
from os import POSIX_FADV_DONTNEED
import pickle, csv, copy
import pandas as pd
import numpy as np
verbs_file = "common_VerbNoun_ptbr.txt"


file_df = pd.read_csv('common_VerbNoun_ptbr.txt', sep='\s', names=['word','lemma','POS_tag'])
nounAdj_df = file_df[file_df['POS_tag'].str.contains('^(N|A).+')].set_index(['lemma'])
prepArt_df = file_df[file_df['POS_tag'].str.contains('^(S8D|D).+')].set_index(['lemma'])
verb_regexes = ['IP', 'II', 'IS', 'IM', 'IF', 'IC', 'SP', 'SI', '(SF|N0)']
verb_df_dict = {}
for verb_regex in verb_regexes:
    verb_df_dict[verb_regex] = file_df[file_df['POS_tag'].str.contains('^'+'VM'+verb_regex+'.+')]\
                                                         .set_index(['lemma'])


#%%

nounAdj_full_listOfArrays = []
NOUNADJ_lemma_values = set(nounAdj_df.index)
for i, lemma in enumerate(NOUNADJ_lemma_values):
    if i%5000 == 0:
        print(i)
    lemma_array = nounAdj_df.loc[lemma].values
    nounAdj_full_listOfArrays.append(lemma_array)
pickle.dump(nounAdj_full_listOfArrays, open("pickle/nounAdj_relations.p","wb"))

Verb_full_listOfArrays = []
for key in verb_df_dict.keys():
    verb_lemma_values = set(verb_df_dict[key].index)
    for i, lemma in enumerate(verb_lemma_values):
        if i%5000 == 0:
            print(i)
        lemma_array = verb_df_dict[key].loc[lemma].values
        if len(lemma_array.shape) == 1:
            continue
        lemma_array = np.concatenate([lemma_array, [[lemma]]*lemma_array.shape[0]], axis=1)
        Verb_full_listOfArrays.append(lemma_array)
pickle.dump(Verb_full_listOfArrays, open("pickle/verb_relations.p","wb"))

prepArt_full_listOfArrays = []
PREPART_lemma_values = set(prepArt_df.index)
for i, lemma in enumerate(PREPART_lemma_values):
    if i%300 == 0:
        print(i)
    lemma_array = prepArt_df.loc[lemma].values
    prepArt_full_listOfArrays.append(lemma_array)
pickle.dump(prepArt_full_listOfArrays, open("pickle/prepArt_relations.p","wb"))


#%% opening the dumps and working their relations



nounAdj_pickle = pickle.load(open('pickle/nounAdj_relations.p', 'rb'))
prepArt_pickle = pickle.load(open('pickle/prepArt_relations.p', 'rb'))
verb_pickle = pickle.load(open('pickle/verb_relations.p', 'rb'))
# create a list for capitalized words such as 'Existem', in the place of 'Existe'.
upper_verb_pickle = []
for verb in copy.deepcopy(verb_pickle):
    upper_first_column = np.array(list(map(lambda x: x.capitalize(), verb[:,0])))
    verb[:,0] = upper_first_column
    upper_verb_pickle.append(verb)



nounAdjdic = {}
for i, nounAdj in enumerate(nounAdj_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in nounAdj[:,0]:
            nounAdj_nodupes = np.array(list(set(nounAdj[:,0])))
            nounAdjdic[word] = list(np.delete(nounAdj_nodupes, np.where(nounAdj_nodupes == word)))
            #print(verbI[:,0])
    except IndexError:
        #print('one row only =>', verbI)
        pass

prepArtdic = {}
for i, prepArt in enumerate(prepArt_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in prepArt[:,0]:
            prepArt_nodupes = np.array(list(set(prepArt[:,0])))
            prepArtdic[word] = list(np.delete(prepArt_nodupes, np.where(prepArt_nodupes == word)))
            #print(verbI[:,0])
    except IndexError:
        #print('one row only =>', verbI)
        pass
        
Vdic = {}
for i, verb in enumerate(verb_pickle + upper_verb_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in verb[:,0]:
            verb_nodupes = np.array(list(set(verb[:,0])))
            verb_deletekeyfromvalue = list(np.delete(verb_nodupes, np.where(verb_nodupes == word)))
            if word not in Vdic.keys():
                Vdic[word] = verb_deletekeyfromvalue
            else:
                Vdic[word] += verb_deletekeyfromvalue
                Vdic[word] = list(set(Vdic[word]))
            if word == 'ad??quo':
                print(verb)
                print(Vdic[word])
#            if word == 'foram':
#                print(verb, verb_nodupes, Vdic[word])
    except IndexError:
        #print('one row only =>', verb)
        pass


#%%
    
def mergeDicts(dict1, dict2):
    full_dict = {}
    for key in dict1.keys():
        if key not in dict2.keys():
            full_dict[key] = dict1[key]
        else:
            full_dict[key] = dict1[key] + dict2[key]
    for key in dict2.keys():
        if key not in dict1.keys():
            full_dict[key] = dict2[key]
        else:
            full_dict[key] = dict2[key] + dict1[key]
    return full_dict

VnounAdjdic = mergeDicts(Vdic, nounAdjdic)
fulldic = mergeDicts(VnounAdjdic, prepArtdic)
    
#%% dumping all relations

pickle.dump(fulldic, open("common_VerbNoun_ptbr.p","wb"))
pickle.dump(Vdic, open("common_Verb_ptbr.p","wb"))


#%%
#####################
### new task ########
#####################
#%% Now we have to work with the relations and their tags so that we dump them to the file verb-form-vocab.txt
### which will have rows such as 'abandon_abandoned:VB_VBD' (taken from english)
#%%

nounAdj_pickle = pickle.load(open('pickle/nounAdj_relations.p', 'rb'))
prepArt_pickle = pickle.load(open('pickle/prepArt_relations.p', 'rb'))
verb_pickle = pickle.load(open('pickle/verb_relations.p', 'rb'))
# create a list for capitalized words such as 'Existem', in the place of 'Existe'.
upper_verb_pickle = []
for verb in copy.deepcopy(verb_pickle):
    upper_first_column = np.array(list(map(lambda x: x.capitalize(), verb[:,0])))
    verb[:,0] = upper_first_column
    upper_verb_pickle.append(verb)

from collections import Counter
import re

Vdetaildic = {}
for i, verb in enumerate(verb_pickle + upper_verb_pickle):
    if i%5000 == 0:
        print(i)
    try:
        # joining 'VM.1S' and 'VM.3S' into 'VM.1SandVM.3S' when both former definitions are for the same word, e.g. 'fazia'
        dupe_words = [item for item, count in Counter(verb[:,0]).items() if count > 1]
        for _ in dupe_words:
            for j, (word, tag, lemma) in enumerate(verb):
                mask_dupe = verb[:,0] == word
                if sum(mask_dupe) > 1:
                    postag = 'and'.join(sorted(list(verb[:,1][mask_dupe])))
                    entry = np.array([word, postag, lemma])
                    verb_deldupes = np.delete(verb, np.where(mask_dupe), 0)
                    verb_joinpos = np.vstack([verb_deldupes, entry])
                    verb = verb_joinpos
                    if word == 'timbrar':
                        print(verb, mask_dupe, sum(mask_dupe))
                    #print(word, verb)
                    break
        # defining the tag 'VM.1SandVM.3S' for all separate 'VM.3S', e.g. 'fazem' (in comparison to 'fa??o')
        for j, (word, tag, lemma) in enumerate(verb):
            regex_3S = re.compile('^VM(..)3S0')
            if regex_3S.search(tag):
                new_tag = 'VM' + regex_3S.search(tag).group(1) + '1S0' + 'and' + 'VM' + regex_3S.search(tag).group(1) + '3S0'
                verb[j][1] = new_tag
        # defining a dictionary with the entry and its substitutes
        for j, (word, tag, lemma) in enumerate(verb):
            verb_nodupes = verb#np.array(list(set(verbI)))
            Vdetaildic[(word,tag,lemma)] = np.delete(verb_nodupes, np.where(verb_nodupes[:,0] == word), 0)
    
    # one row only, so no substitutions
    except (IndexError, ValueError) as e:
        pass

    

#%%

### this Vdetaildic was when we did not have the same word with different postags. In
### the implementation above, we managed to join the postags of that duplicate word.
#Vdetaildic = {}
#for i, verb in enumerate(verb_pickle):
#    if i%5000 == 0:
#        print(i)
#    try:
#        for j, (word, tag) in enumerate(verb):
#            verb_nodupes = verb#np.array(list(set(verbI)))
#            Vdetaildic[(word,tag)] = np.delete(verb_nodupes, np.where(verb_nodupes[:,0] == word), 0)
#            #print(verbI[:,0])
#    except (IndexError, ValueError) as e:
#        #print('one row only =>', verbI)
#        pass

nounAdjdetaildic = {}
for i, nounAdj in enumerate(nounAdj_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for j, (word, tag) in enumerate(nounAdj):
            nounAdj_nodupes = nounAdj#np.array(list(set(verbI)))
            nounAdjdetaildic[(word,tag)] = np.delete(nounAdj_nodupes, np.where(nounAdj_nodupes[:,0] == word), 0)
            #print(verbI[:,0])
    except (IndexError, ValueError) as e:
        #print('one row only =>', verbI)
        pass

prepArtdetaildic = {}
for i, prepArt in enumerate(prepArt_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for j, (word, tag) in enumerate(prepArt):
            prepArt_nodupes = prepArt#np.array(list(set(verbI)))
            prepArtdetaildic[(word,tag)] = np.delete(prepArt_nodupes, np.where(prepArt_nodupes[:,0] == word), 0)
            #print(verbI[:,0])
    except (IndexError, ValueError) as e:
        #print('one row only =>', verbI)
        pass


#%% joining and dumping the verb-form-vocab.txt

verb_form_vocab_list = []
### nouns and adjs
#for i, (word, tag) in enumerate(nounAdjdetaildic.keys()):
#    value = nounAdjdetaildic[(word, tag)]
#    value_shape_0 = value.shape[0]
#    for word_tag in nounAdjdetaildic[(word, tag)]:
#        words_tags_str = word + '_' + word_tag[0] + ':' + tag[:4] + '_' + word_tag[1][:4]
#        verb_form_vocab_list.append(words_tags_str)
### prepositions and articles
#for i, (word, tag) in enumerate(prepArtdetaildic.keys()):
#    value = prepArtdetaildic[(word, tag)]
#    value_shape_0 = value.shape[0]
#    for word_tag in prepArtdetaildic[(word, tag)]:
#        if 'S8D' in tag:
#            first_tag = tag[:3]+tag[5:7]
#            second_tag = word_tag[1][:3]+word_tag[1][5:7]
#        else:
#            first_tag = tag[:1]+tag[3:5]
#            second_tag = word_tag[1][:1]+word_tag[1][3:5]
#            
#        words_tags_str = word + '_' + word_tag[0] + ':' + first_tag + '_' + second_tag
#        verb_form_vocab_list.append(words_tags_str)
# verbs
for i, (word, tag, lemma) in enumerate(Vdetaildic.keys()):
    value = Vdetaildic[(word, tag, lemma)]
    value_shape_0 = value.shape[0]
    for word_tag_lemma in Vdetaildic[(word, tag, lemma)]:
        if len(tag) > 10:
            first_tag = tag[:3]+tag[4:6] + 'and' + tag[10:13]+tag[14:16]
        else:
            first_tag = tag[:3]+tag[4:6]
        if len(word_tag_lemma[1]) > 10:
            second_tag = word_tag_lemma[1][:3]+word_tag_lemma[1][4:6] + 'and' + word_tag_lemma[1][10:13]+word_tag_lemma[1][14:16]
        else:
            second_tag = word_tag_lemma[1][:3]+word_tag_lemma[1][4:6]
        if first_tag == second_tag: # we do not want to correct different spellings of the same word
            #print((word, tag, lemma), Vdetaildic[(word, tag, lemma)])
            print(word, tag, lemma)
            continue
        words_tags_str = word + '_' + word_tag_lemma[0] + ':' + first_tag + '_' + second_tag
        verb_form_vocab_list.append(words_tags_str)

#%% sorting by frequency on the second word, i.e. the word2 in "word1_word2:tag1_tag2"
from create_freq_dataframe import freq_df

separate_word_list = []
for vfv in verb_form_vocab_list:
    words = vfv.split(":")[0]
    tags = vfv.split(":")[1]
    word1 = words.split("_")[0]
    word2 = words.split("_")[1]
    separate_word_list.append([word1,word2,tags])

separate_word_df = pd.DataFrame(separate_word_list, columns=['word1', 'word2', 'POStags'])
freq_df = freq_df.reset_index()

merged = separate_word_df.merge(freq_df, left_on='word2', right_on='word', how='left')
merged['index'] = merged['index'].fillna(value=max(merged['index'])+1)
merged = merged.sort_values(by='index').drop(['index','word'], axis=1)
merged['vfv'] = merged['word1'] + '_' + merged['word2'] + ':' + merged['POStags']

#%%
#verb_form_vocab_df = pd.DataFrame(verb_form_vocab_list)
verb_form_vocab_df = merged['vfv']
verb_form_vocab_df.to_csv('verb-form-vocab.txt', index=False, header=False, sep='\t', quoting=csv.QUOTE_NONE)

#%% check redundancies

from collections import defaultdict


labelsdic = defaultdict(list)
for e in verb_form_vocab_list:
    words, labels = e.split(':')
    word1, word2 = words.split('_')
    if 'mosV' in word1+labels:
        continue
    labelsdic[word1 + labels].append(word2)

uniquedic = defaultdict(list)
for f in labelsdic:
    if len(labelsdic[f]) < 2:
        continue
    uniquedic[f] = labelsdic[f]






#%%


freq_df





























# %%
