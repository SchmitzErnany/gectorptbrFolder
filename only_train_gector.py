#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 16:53:39 2021

@author: ernanyschmitz
"""
#%%

!python3 train.py --batch_size 16 --vocab_path data/output_vocabulary \
--train_set files/neural_files/train_50.txt --dev_set files/neural_files/test_50.txt \
--model_dir MODEL_DIR --transformer_model bertimbaubase --lowercase_tokens 0 --n_epoch 20

#%%
--vocab_path data/output_vocabulary 

#%%

#source_tokens = 'Ela é amnésica e está sendo caçada pelos purificadores.'.split()
#incorr_tokens = 'Ela e amnésica é está sendo caçada pelos purificadores.'.split()
#
#from difflib import SequenceMatcher
#matcher = SequenceMatcher(None, source_tokens, incorr_tokens)
#diffs = list(matcher.get_opcodes())
#
#diffs