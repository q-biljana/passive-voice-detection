#
# Text_analysis.py
# this file contains the NLP libraries for English, language 
# 
from __future__ import division
import os
import re
import operator
import nltk
import json 

#### List of dictionaries used for 
"""
	Define regex objects which clean the text for analysis by nltk  
"""
quotation_re = re.compile(u'[\u00AB\u00BB\u201C\u201D\u201E\u201F\u2033\u2036\u301D\u301E]')
apostrophe_re = re.compile(u'[\u02BC\u2019\u2032]')
punct_error_re = re.compile('^(["\]\)\}]+)(?:[ \n]|$)')
ellipsis_re = re.compile('\.\.\.["\(\)\[\]\{\} ] [A-Z]')
newline_re = re.compile('\n["\(\[\{ ]*[A-Z]')
empty_sent_re = re.compile('^[\n ]*$')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')



def analyze_text(json_content):
    # create data and metrics dictionaries
    data = dict()
    metrics = dict()

    ### parse text/json string
    original_text = json.loads(json.dumps(json_content))

    # standardize all quotation marks
    text = quotation_re.sub('"', original_text)
    text = apostrophe_re.sub("'", text)

    # tokenize text into sentences
    text_eg_ie = text.replace('e.g.', 'e.---g.').replace('i.e.', 'i.---e.')
    sents_draft = nltk.sent_tokenize(text_eg_ie)
    for idx, sent in enumerate(sents_draft[:]):
        sents_draft[idx] = sents_draft[idx].replace('e.---g.', 'e.g.').replace('i.---e.', 'i.e.')
        if idx > 0:
            punct_error = punct_error_re.findall(sent)
            if punct_error:
                sents_draft[idx-1] += punct_error[0]
                sents_draft[idx] = sents_draft[idx][len(punct_error[0])+1:]

    # separate sentences at ellipsis characters correctly
    sents_draft_2 = []
    for sent in sents_draft:
        idx = 0
        for ellipsis_case in ellipsis_re.finditer(sent):
            sents_draft_2.append(sent[idx:(ellipsis_case.start() + 3)])
            idx = ellipsis_case.start() + 3
        sents_draft_2.append(sent[idx:])

    sents = []
    for sent in sents_draft_2:
        idx = 0
        for newline_case in newline_re.finditer(sent):
            sents.append(sent[idx:(newline_case.start() + 1)])
            idx = newline_case.start() + 1
        sents.append(sent[idx:])

    # delete empty sentences
    sents = [sent for sent in sents if not empty_sent_re.match(sent)]

    # tokenize sentences into words and punctuation marks
    sents_tokens = [nltk.word_tokenize(sent) for sent in sents]
    tokens = [token for sent in sents_tokens for token in sent]
    data['sentence_numbers'] = [(idx+1) for idx, sent in enumerate(sents_tokens) for token in sent]

    # tag tokens as part-of-speech
    sents_tokens_tags = nltk.pos_tag(sents_tokens[0])
    # data['parts_of_speech'] = [pos for sent in sents_tokens_tags for (token, pos) in sent]
    data['parts_of_speech'] = [pos for token, pos in sents_tokens_tags]

    # fix symbol and apostrophed verb tags
    for idx, token in enumerate(tokens):
        if not token[0].isalnum():
            if token in ["'m", "'re", "'ve"]:
                data['parts_of_speech'][idx] = 'VBP'
            elif token == "'s":
                if data['parts_of_speech'][idx] != 'POS':
                    data['parts_of_speech'][idx] = 'VBP'
            elif token == "'d":
                data['parts_of_speech'][idx] = 'VBD'
            elif token == "'ll":
                data['parts_of_speech'][idx] = 'MD'
            elif data['parts_of_speech'][idx].isalnum():
                data['parts_of_speech'][idx] = 'SYM'

    # fix some verbs ending in -ing being counted as nouns
    for idx, token in enumerate(tokens):
        if (token[-3:] == 'ing') and (idx < len(tokens)) and (data['parts_of_speech'][idx+1] == 'IN'):
            data['parts_of_speech'][idx] = 'VBG'

    # find verb groups
    data['verb_groups'] = [None] * len(tokens)
    verb_group_stack = []
    verb_group_count = 0
    for idx, token in enumerate(tokens):
        if not verb_group_stack:
            if token in ["be", "am", "'m", "is", "'s", "are", "'re", "was", "were", "will", "'ll", "wo", "have", "'ve", "has", "had"]:
                verb_group_stack.append(idx)
        elif token in ['be', 'been', 'being', 'have', 'had']:
            verb_group_stack.append(idx)
        elif data['parts_of_speech'][idx][:2] == 'VB':
            verb_group_stack.append(idx)
            verb_group_count += 1
            for i in verb_group_stack:
                data['verb_groups'][i] = verb_group_count
            verb_group_stack = []
        elif data['parts_of_speech'][idx][:2] not in ['RB', 'PD']:
            if len(verb_group_stack) > 1:
                verb_group_count += 1
                for i in verb_group_stack:
                    data['verb_groups'][i] = verb_group_count
            verb_group_stack = []


    ### compute metrics on parsed data
    # count number of sentences
    metrics['sentence_count'] = len(sents)

    # find and count passive voice cases
    data['passive_voice_cases'] = [None] * len(tokens)
    passive_voice_count = 0
    for i in range(verb_group_count):
        verb_group_stack = [idx for idx in range(len(tokens)) if data['verb_groups'][idx] == i+1]
        if data['parts_of_speech'][verb_group_stack[-1]] in ['VBN', 'VBD']:
            for j in verb_group_stack[:-1]:
                if tokens[j] in ["am", "'m", "is", "'s", "are", "'re", "was", "were", "be", "been", "being"]:
                    passive_voice_count += 1
                    data['passive_voice_cases'][j] = passive_voice_count
                    data['passive_voice_cases'][verb_group_stack[-1]] = passive_voice_count
                    break
    if metrics['sentence_count']:
        metrics['passive_voice_ratio'] = passive_voice_count / metrics['sentence_count']
    else:
        metrics['passive_voice_ratio'] = 0


    return original_text, data, metrics, tokens
