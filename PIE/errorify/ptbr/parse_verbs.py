import pickle
import pandas as pd
import numpy as np
verbs_file = "common_VerbNoun_ptbr.txt"


file_df = pd.read_csv('common_VerbNoun_ptbr.txt', sep='\s', names=['word','lemma','POS_tag'])
nounAdj_df = file_df[file_df['POS_tag'].str.contains('^(N|A).+')].set_index(['lemma'])
verb_I_df = file_df[file_df['POS_tag'].str.contains('^VM[I].+')].set_index(['lemma'])
verb_NS_df = file_df[file_df['POS_tag'].str.contains('^VM[NS].+')].set_index(['lemma'])
NOUNADJ_lemma_values = nounAdj_df.index
VerbI_lemma_values = verb_I_df.index
VerbNS_lemma_values = verb_NS_df.index

#%%

nounAdj_full_listOfArrays = []
for i, lemma in enumerate(NOUNADJ_lemma_values):
    if i%100 == 0:
        print(i)
    lemma_array = nounAdj_df.loc[lemma].values
    nounAdj_full_listOfArrays.append(lemma_array)
#pickle.dump(nounAdj_full_listOfArrays, open("pickle/nounAdj_relations.p","wb"))
#%%

VerbI_full_listOfArrays = []
for i, lemma in enumerate(VerbI_lemma_values):
    if i%100 == 0:
        print(i)
    lemma_array = verb_I_df.loc[lemma].values
    VerbI_full_listOfArrays.append(lemma_array)
pickle.dump(VerbI_full_listOfArrays, open("pickle/verbI_relations.p","wb"))


VerbNS_full_listOfArrays = []
for i, lemma in enumerate(VerbNS_lemma_values):
    if i%100 == 0:
        print(i)
    lemma_array = verb_NS_df.loc[lemma].values
    VerbNS_full_listOfArrays.append(lemma_array)
pickle.dump(VerbNS_full_listOfArrays, open("pickle/verbNS_relations.p","wb"))


#%% opening the dumps and working their relations

nounAdj_pickle = pickle.load(open('pickle/nounAdj_relations.p', 'rb'))
verbI_pickle = pickle.load(open('pickle/verbI_relations.p', 'rb'))
verbNS_pickle = pickle.load(open('pickle/verbNS_relations.p', 'rb'))


Idic = {}
for i, verbI in enumerate(verbI_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in verbI[:,0]:
            verbI_nodupes = np.array(list(set(verbI[:,0])))
            Idic[word] = list(np.delete(verbI_nodupes, np.where(verbI_nodupes == word)))
            #print(verbI[:,0])
    except IndexError:
        #print('one row only =>', verbI)
        pass

NSdic = {}
for i, verbNS in enumerate(verbNS_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for word in verbNS[:,0]:
            verbNS_nodupes = np.array(list(set(verbNS[:,0])))
            NSdic[word] = list(np.delete(verbNS_nodupes, np.where(verbNS_nodupes == word)))
            #print(verbI[:,0])
    except IndexError:
        #print('one row only =>', verbI)
        pass
    
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

INSdic = mergeDicts(Idic, NSdic)
fulldic = mergeDicts(INSdic, nounAdjdic)
    
#%% dumping all relations

pickle.dump(fulldic, open("common_VerbNoun_ptbr.p","wb"))


#####################
### new task ########
#####################
#%% Now we have to work with the relations and their tags so that we dump them to the file verb-form-vocab.txt
#%% which will have rows such as 'abandon_abandoned:VB_VBD' (taken from english)
#%%

nounAdj_pickle = pickle.load(open('pickle/nounAdj_relations.p', 'rb'))
verbI_pickle = pickle.load(open('pickle/verbI_relations.p', 'rb'))
verbNS_pickle = pickle.load(open('pickle/verbNS_relations.p', 'rb'))


Idetaildic = {}
for i, verbI in enumerate(verbI_pickle):
    if i%5000 == 0:
        print(i)
    try:
        for j, (word, tag) in enumerate(verbI):
            verbI_nodupes = verbI#np.array(list(set(verbI)))
            Idetaildic[(word,tag)] = np.delete(verbI_nodupes, np.where(verbI_nodupes[:,0] == word), 0)
            #print(verbI[:,0])
    except (IndexError, ValueError) as e:
        #print('one row only =>', verbI)
        pass

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



