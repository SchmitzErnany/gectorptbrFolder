"""Synthetic data generator."""
import math
import pickle
import random
from numpy.random import choice as npchoice
import numpy as np

VERBS = pickle.load(open('common_Verb_ptbr.p', 'rb'))  # pickle.load(open('common_VerbNoun_ptbr.p', 'rb')) # we comment out the code that called (N|A|S8D|D).+

COMMON_INSERTS = set(pickle.load(open('common_inserts_ptbr.p', 'rb')))
if COMMON_INSERTS == set():
	COMMON_INSERTS = []

COMMON_REPLACES = pickle.load(open('common_replaces_ptbr.p', 'rb'))
if COMMON_REPLACES == {}:
	COMMON_REPLACES = []

COMMON_DELETES = pickle.load(open('common_deletes_ptbr.p','rb'))
if COMMON_DELETES == {}:
	COMMON_DELETES = []





class Errorifier:
    """Generate errors in good sentences!"""

    def __init__(self, sentence: str):
        self.original_sentence = sentence.rstrip()
        self.sentence = self.original_sentence
        self.tokenized = None
        self.tokenize()

    def tokenize(self):
        self.tokenized = self.sentence.split()

    def correct(self):
        return self.original_sentence

    def no_error(self):
        return ' '.join(self.tokenized)


    def delete_error(self):
        if COMMON_DELETES == []:
            return ' '.join(self.tokenized)

        if len(self.tokenized) > 0:
            insertable = list(range(len(self.tokenized)))
            index = random.choice(insertable)
            

            plist = list(COMMON_DELETES.values())
            plistsum = sum(plist)
            plist = [x / plistsum for x in plist]

            # Choose a bad word
            ins_word = npchoice(list(COMMON_DELETES.keys()), p=plist)
            self.tokenized.insert(index,ins_word)

        return ' '.join(self.tokenized)


    def insert_error(self):
        """Delete a commonly inserted word."""
        if COMMON_INSERTS == []:
            return ' '.join(self.tokenized)

        if len(self.tokenized) > 1:
            insertable = [i for i, w in enumerate(self.tokenized) if w in COMMON_INSERTS]
            if not insertable:
                return self.sentence

            index = random.choice(insertable)
            del self.tokenized[index]
        return ' '.join(self.tokenized)


    def replace_error(self, redir=True):
        """Add a common replace error."""
        if COMMON_REPLACES == []:
            return ' '.join(self.tokenized)

        if len(self.tokenized) > 0:
            replaceable = [i for i, w in enumerate(self.tokenized) if w in COMMON_REPLACES]
            if not replaceable:
                if redir:
                    return self.verb_error(redir=False)
                return self.sentence

            index = random.choice(replaceable)
            word = self.tokenized[index]
            if not COMMON_REPLACES[word]:
                return self.sentence

            # Normalize probabilities
            plist = list(COMMON_REPLACES[word].values())
            plistsum = sum(plist)
            plist = [x / plistsum for x in plist]

            # Choose a bad word
            repl = npchoice(list(COMMON_REPLACES[word].keys()), p=plist)
            self.tokenized[index] = repl

        return ' '.join(self.tokenized)


    def verb_error(self, redir=True):
        """Introduce a verb error from common_VerbNoun_ptbr.p."""
        # sentence_original = self.tokenized[:]
        if VERBS == []:
            return ' '.join(self.tokenized)

        if len(self.tokenized) > 0:
            verbs = [i for i, w in enumerate(self.tokenized) if w in VERBS]
            if not verbs:
                if redir:
                    return self.replace_error(redir=False)
                return self.sentence

            for index in verbs:
                if random.random() > 0.7:
                    continue
                word = self.tokenized[index]
                if not VERBS[word]:
                    continue
                repl = random.choice(VERBS[word])
                #print(word, verbs, VERBS[word], repl)
                self.tokenized[index] = repl

            # index = random.choice(verbs)
            # word = self.tokenized[index]
            # if not VERBS[word]:
            #     return self.sentence
            #repl = random.choice(VERBS[word])
            
            #self.tokenized[index] = repl

        return ' '.join(self.tokenized)


    def error(self):
        """Introduce a random error."""

        changes = [VERBS, COMMON_REPLACES, COMMON_INSERTS, COMMON_DELETES]; change_probs  = [0.5,0.5,.0,0.]; identifiers = [i for i in range(len(changes))];
        multiple_index = {}; which_index_true = []; count_verb=0; count_replace=0;
        if len(self.tokenized) > 0:
            for i, w in enumerate(self.tokenized):
                mi = [False]*len(changes); count = 0
                if w in VERBS and change_probs[0] > 0:
                    mi[0] = True; count += 1;
                if w in COMMON_REPLACES and change_probs[1] > 0:
                    mi[1] = True; count += 1;
                if w in COMMON_INSERTS and change_probs[2] > 0:
                    mi[2] = True; count += 1;
                if w in COMMON_DELETES and change_probs[3] > 0:
                    mi[3] = True; count += 1;

                multiple_index[i] = mi
                if count > 0:
                    which_index_true.append(i)

            for index in which_index_true:
                if random.random() > 0.7:
                    continue
                word = self.tokenized[index]
                mask_which_change_true = np.array(multiple_index[index])
                
                new_probs = np.array(change_probs)[mask_which_change_true]
                new_identifiers = np.array(identifiers)[mask_which_change_true]
                change_id = npchoice(new_identifiers, p=new_probs/sum(new_probs))
                if change_id == 1:
                    repl_list = list(changes[change_id][word].keys())
                elif change_id == 0:
                    repl_list = changes[change_id][word]
                if not repl_list:
                    print('WARNING: does not contain replacements!')
                    continue
                repl = random.choice(repl_list)
                self.tokenized[index] = repl
                # if word == 'da' and repl != 'dá':
                #     print(change_id, word, repl_list, repl, self.tokenized)

        self.sentence = ' '.join(self.tokenized)
        self.tokenize()


        return self.sentence
