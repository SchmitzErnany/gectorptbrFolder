#%%
"""Synthetic data generator."""
import math
import pickle
import random
from numpy.random import choice as npchoice
import numpy as np

VERBS = pickle.load(
    open("common_Verb_ptbr.p", "rb")
)  # pickle.load(open('common_VerbNoun_ptbr.p', 'rb')) # we comment out the code that called (N|A|S8D|D).+

COMMON_REPLACES = pickle.load(open("common_replaces_ptbr.p", "rb"))
if COMMON_REPLACES == {}:
    COMMON_REPLACES = []

COMMON_TO_BE_INSERTED = pickle.load(open("common_inserts_ptbr.p", "rb"))
if COMMON_TO_BE_INSERTED == {}:
    COMMON_TO_BE_INSERTED = []

COMMON_TO_BE_DELETED = pickle.load(open("common_deletes_ptbr.p", "rb"))
if COMMON_TO_BE_DELETED == {}:
    COMMON_TO_BE_DELETED = []


print(pickle.load(open("common_inserts_ptbr.p", "rb")))
print(pickle.load(open("common_deletes_ptbr.p", "rb")))
print(pickle.load(open("common_replaces_ptbr.p", "rb")))

print(COMMON_TO_BE_INSERTED)
print(COMMON_TO_BE_DELETED)
print(COMMON_REPLACES)


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
        return " ".join(self.tokenized)

    def delete_error(self):
        if COMMON_TO_BE_DELETED == []:
            return " ".join(self.tokenized)

        if len(self.tokenized) > 0:
            insertable = list(range(len(self.tokenized)))
            index = random.choice(insertable)

            plist = list(COMMON_TO_BE_DELETED.values())
            plistsum = sum(plist)
            plist = [x / plistsum for x in plist]

            # Choose a bad word
            ins_word = npchoice(list(COMMON_TO_BE_DELETED.keys()), p=plist)
            self.tokenized.insert(index, ins_word)

        return " ".join(self.tokenized)

    def insert_error(self):
        """Delete a commonly inserted word."""
        if COMMON_TO_BE_INSERTED == []:
            return " ".join(self.tokenized)

        if len(self.tokenized) > 1:
            insertable = [
                i for i, w in enumerate(self.tokenized) if w in COMMON_TO_BE_INSERTED
            ]
            if not insertable:
                return self.sentence

            index = random.choice(insertable)
            del self.tokenized[index]
        return " ".join(self.tokenized)

    def replace_error(self, redir=True):
        """Add a common replace error."""
        if COMMON_REPLACES == []:
            return " ".join(self.tokenized)

        if len(self.tokenized) > 0:
            replaceable = [
                i for i, w in enumerate(self.tokenized) if w in COMMON_REPLACES
            ]
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

        return " ".join(self.tokenized)

    def verb_error(self, redir=True):
        """Introduce a verb error from common_VerbNoun_ptbr.p."""
        # sentence_original = self.tokenized[:]
        if VERBS == []:
            return " ".join(self.tokenized)

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
                # print(word, verbs, VERBS[word], repl)
                self.tokenized[index] = repl

            # index = random.choice(verbs)
            # word = self.tokenized[index]
            # if not VERBS[word]:
            #     return self.sentence
            # repl = random.choice(VERBS[word])

            # self.tokenized[index] = repl

        return " ".join(self.tokenized)

    def error(self):
        """Introduce a random error."""

        changes = [VERBS, COMMON_REPLACES, COMMON_TO_BE_INSERTED, COMMON_TO_BE_DELETED]
        change_probs = [0.4, 0.4, 0.1, 0.1]
        id_to_repl_kind = {
            0: "verbs",
            1: "replaces",
            2: "to_be_inserted",
            3: "to_be_deleted",
        }
        identifiers = list(id_to_repl_kind.keys())
        multiple_index = {}
        which_index_true = []
        if len(self.tokenized) > 0:
            for i, w in enumerate(self.tokenized):
                mi = [False] * len(changes)
                count = 0
                if w in VERBS and change_probs[0] > 0:
                    mi[0] = True
                    count += 1
                if w in COMMON_REPLACES and change_probs[1] > 0:
                    mi[1] = True
                    count += 1
                # this one is specific for punctuation, which is present at the end of a certain token.
                # If the tokenizer is the .split() method, the punctuation is gonna be coupled to the
                # token. That is why we take the last character from the word (this last character
                # is punctuation) and check whether it is in the list COMMON_TO_BE_INSERTED.
                if w[-1] in COMMON_TO_BE_INSERTED and change_probs[2] > 0:
                    mi[2] = True
                    count += 1
                # this one is peculiar because we are going to insert elements which will be later deleted.
                if change_probs[3] > 0 and random.random() > 0.9:
                    mi[3] = True
                    count += 1

                multiple_index[i] = mi
                if count > 0:
                    which_index_true.append(i)

            for index in which_index_true:
                if random.random() > 0.7:
                    continue
                word = self.tokenized[index]
                mask_which_change_true = np.array(multiple_index[index])

                probs_with_change = np.array(change_probs)[mask_which_change_true]
                identifiers_with_change = np.array(identifiers)[mask_which_change_true]
                change_id = npchoice(
                    identifiers_with_change,
                    p=probs_with_change / sum(probs_with_change),
                )
                repl_kind = id_to_repl_kind[change_id]
                if repl_kind == "verbs":
                    repl_list = changes[change_id][word]
                elif repl_kind == "replaces":
                    repl_list = list(changes[change_id][word].keys())
                elif repl_kind == "to_be_inserted":
                    punct = word[-1]
                    possible_puncts_to_remove_from_word = list(
                        changes[change_id].keys()
                    )
                    if punct in possible_puncts_to_remove_from_word:
                        word_without_punct = word[:-1]
                        repl_list = [word_without_punct]
                elif repl_kind == "to_be_deleted":
                    possible_puncts_to_add_to_word = list(changes[change_id].keys())
                    repl_list = np.core.defchararray.add(word, possible_puncts_to_add_to_word)

                if not repl_list:
                    print(f'WARNING: the word "{word}" does not contain replacements!')
                    continue
                repl = random.choice(repl_list)

                # if the replacement is equal to a token which appears nearby, continue the loop.
                window = 3
                if (
                    index >= window
                    and repl
                    in self.original_sentence.split()[
                        index - window : index + window + 1
                    ]
                ):
                    continue

                # finalling replacing the tokens for replacements.
                if any(repl_kind == kind for kind in ["verbs", "replaces"]):
                    self.tokenized[index] = repl
                elif repl_kind == "to_be_inserted":
                    self.tokenized[index] = repl
                elif repl_kind == "to_be_deleted":
                    self.tokenized[index] = repl

        self.sentence = " ".join(self.tokenized)
        self.tokenize()

        return self.sentence


# %%
# puncts = [",", "."]
# word = ["nois"]
# rep = np.core.defchararray.add(word, puncts)
# # %%
# random.choice(rep)

# %%
