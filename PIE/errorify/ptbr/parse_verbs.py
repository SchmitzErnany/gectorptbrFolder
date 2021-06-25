import pickle, csv
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
NOUNADJ_lemma_values = nounAdj_df.index
for i, lemma in enumerate(NOUNADJ_lemma_values):
    if i%5000 == 0:
        print(i)
    lemma_array = nounAdj_df.loc[lemma].values
    nounAdj_full_listOfArrays.append(lemma_array)
pickle.dump(nounAdj_full_listOfArrays, open("pickle/nounAdj_relations.p","wb"))
#%%

Verb_full_listOfArrays = []
for key in verb_df_dict.keys():
    verb_lemma_values = verb_df_dict[key].index
    for i, lemma in enumerate(verb_lemma_values):
        if i%1000 == 0:
            print(i)
        lemma_array = verb_df_dict[key].loc[lemma].values
        Verb_full_listOfArrays.append(lemma_array)
pickle.dump(Verb_full_listOfArrays, open("pickle/verb_relations.p","wb"))

prepArt_full_listOfArrays = []
PREPART_lemma_values = prepArt_df.index
for i, lemma in enumerate(PREPART_lemma_values):
    if i%5000 == 0:
        print(i)
    lemma_array = prepArt_df.loc[lemma].values
    prepArt_full_listOfArrays.append(lemma_array)
pickle.dump(prepArt_full_listOfArrays, open("pickle/prepArt_relations.p","wb"))
#%% opening the dumps and working their relations

nounAdj_pickle = pickle.load(open('pickle/nounAdj_relations.p', 'rb'))
prepArt_pickle = pickle.load(open('pickle/prepArt_relations.p', 'rb'))
verb_pickle = pickle.load(open('pickle/verb_relations.p', 'rb'))


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
for i, verb in enumerate(verb_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in verb[:,0]:
            verb_nodupes = np.array(list(set(verb[:,0])))
            Vdic[word] = list(np.delete(verb_nodupes, np.where(verb_nodupes == word)))
            #print(verbI[:,0])
    except IndexError:
        #print('one row only =>', verbI)
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


Vdetaildic = {}
for i, verb in enumerate(verb_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for j, (word, tag) in enumerate(verb):
            verb_nodupes = verb#np.array(list(set(verbI)))
            Vdetaildic[(word,tag)] = np.delete(verb_nodupes, np.where(verb_nodupes[:,0] == word), 0)
            #print(verbI[:,0])
    except (IndexError, ValueError) as e:
        #print('one row only =>', verbI)
        pass
    
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
for i, (word, tag) in enumerate(Vdetaildic.keys()):
    value = Vdetaildic[(word, tag)]
    value_shape_0 = value.shape[0]
    for word_tag in Vdetaildic[(word, tag)]:
        words_tags_str = word + '_' + word_tag[0] + ':' + tag[:3]+tag[4:6] + '_' + word_tag[1][:3]+word_tag[1][4:6]
        verb_form_vocab_list.append(words_tags_str)

verb_form_vocab_df = pd.DataFrame(verb_form_vocab_list)
verb_form_vocab_df.to_csv('verb-form-vocab.txt', index=False, header=False, sep='\t', quoting=csv.QUOTE_NONE)













#%%

#def expand_dict(d):
#    result = {}
#    for key in d:
#        if key in result:
#            result[key] = result[key].union(d[key].difference({key}))
#        else:
#            result[key] = d[key].difference({key})
#        for item in d[key]:
#            if item in result:
#                if item != key:
#                    result[item] = result[item].union(d[key].difference({item})).union({key})
#                else:
#                    result[item] = result[item].union(d[key].difference({item}))
#            else:
#                if item != key:
#                    result[item] = d[key].difference({item}).union({key})
#                else:
#                    d[key].difference({item})
#
#    
#    for key in result:
#        result[key]=list(result[key])
#    return result
#
#
#with open(verbs_file,"r") as ip_file:
#    ip_lines = ip_file.readlines()
#    words = {}
#    for line in ip_lines:
#        line = line.strip().split()
#        if len(line) != 3:
#            print(line)
#        word = line[1]
#        word_form = line[0]
#        if word in words:
#            words[word].add(word_form)
#        else:
#            words[word]={word_form}
#
#
#result = expand_dict(words)
#pickle.dump(result,open("common_VerbNoun_ptbr.p","wb"))


#%%



